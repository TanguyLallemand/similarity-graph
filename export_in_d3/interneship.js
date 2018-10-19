//Define variable to group SVG objects
var vis = svgRoot.append("g");

//Define zoom behavior
var zoom = d3.behavior.zoom()
    .scaleExtent([1, 10])
    .on("zoom", zoomed);

d3.select("svg")
    .call(zoom);

//Function to handle with zoom
function zoomed() {
    var translation = d3.event.translate,
        scale = d3.event.scale;
    //Set contraint to pan and zoom.
    //First number is max possible, if user try to pan or zoom above this number translation will be set to this number
    translation[0] = Math.max(-180, Math.min(translation[0], width - scale * 50));
    translation[1] = Math.max(-180, Math.min(translation[1], height - scale * 50));
    //Transform translation array in a object of translation
    zoom.translate(translation);
    d3.select(".drawarea").attr("transform", "translate(" + translation + ")scale(" + scale + ")");
}
},

/**
 * Call Method to refresh the Network
 *
 * @param data {data} Datas abbout all relations and concept to represent
 * @param width {witdh} witdh of SVG constructed
 * @param height {height} height of SVG constructed
 * @param mapping {mapping} dictionnary containing index of concept in array and id of concept related
 * @param arrayOfColor {arrayOfColor} Array with color selected
 */
update: function(data, width, height, mapping, arrayOfColor) {

        //Set different variables
        var color = d3.scale.ordinal().range(arrayOfColor);
        var vis = svgRoot.append("g");

        //Variable for detection of collision
        var padding = 1, // separation between circles
            radius = 8;

        //Set up the force layout
        var force = d3.layout.force()
            .size([width - 50, height])
            .linkDistance(90)
            .charge(-225)
            .friction(0.95);

        //Stock data to send it to createNodesandLinks()
        var dataNodes = data.nodes;
        var dataLinks = data.links;
        //
        //Generate links and nodes
        //
        var svgObjects = this.createNodesandLinks(vis, dataLinks, dataNodes, color, mapping);
        //Parse data returned
        var path = svgObjects[0];
        var pathInvis = svgObjects[1];
        var node = svgObjects[2];
        var label = svgObjects[3];

        //Construct legend using color used for links
        this.buildLegend(svgRoot, color, width);

        //Check for empty links before start simulation
        if (this.hasEmptyElement(dataLinks)) {
            //start simulation
            if (data.nodes[0] != undefined && typeof data.links[0].source !== 'undefined') { //Check if nodes data are not null and if links data are not null
                force
                    .nodes(d3.values(data.nodes))
                    .links(data.links)
                    .on("tick", ticked)
                    .start();
            }
        }


        //The force layout is generating the coordinates of SVG elements
        function ticked() {
            if (data.nodes[0] != undefined && typeof data.links[0].source !== 'undefined') { //Check if nodes data are not null and if links data are not null
                //fix center on the first node
                data.nodes[0].x = width / 2;
                data.nodes[0].y = height / 2;
                //Calculate every path tought arcPath function
                path.attr("d", function(d) {
                    return arcPath(true, d);
                });
                pathInvis.attr("d", function(d) {
                    return arcPath(d.source.x < d.target.x, d);
                });

                //Calculate node's coordinates
                node.attr("cx", function(d) {
                        return d.x = Math.max(radius, Math.min(width - 10 - radius, d.x)); //permit to constrain nodes into SVG box, with a limit of width + 10 px
                    })
                    .attr("cy", function(d) {
                        return d.y = Math.max(radius, Math.min(height - 10 - radius, d.y)); //permit to constrain nodes into SVG box, with a limit of height + 10 px
                    });
                //Detection of collision between nodes
                node.each(collide(0.5));
                //Calculate label's coordinates
                label.attr("x", function(d) {
                        return d.x;
                    })
                    .attr("y", function(d) {
                        return d.y;
                    })
                //Detection of collision between links
                label.each(collide(0.5));
            }
        };

        //Count how many links have a node
        var countSiblingLinks = function(source, target) {
            var count = 0;
            for (var i = 0; i < data.links.length; ++i) {
                if ((data.links[i].source.Id == source.Id && data.links[i].target.Id == target.Id) || (data.links[i].source.Id == target.Id && data.links[i].target.Id == source.Id))
                    count++;
            };
            return count;
        };

        //Determine labels of different links bounded with the same node
        var getSiblingLinks = function(source, target) {
            var siblings = [];
            for (var i = 0; i < data.links.length; ++i) {
                if ((data.links[i].source.Id == source.Id && data.links[i].target.Id == target.Id) || (data.links[i].source.Id == target.Id && data.links[i].target.Id == source.Id))
                    siblings.push(data.links[i].relation.Description);
            };
            return siblings;
        };

        //Function to build curved links
        function arcPath(leftHand, d) {
            var x1 = leftHand ? d.source.x : d.target.x,
                y1 = leftHand ? d.source.y : d.target.y,
                x2 = leftHand ? d.target.x : d.source.x,
                y2 = leftHand ? d.target.y : d.source.y,
                dx = x2 - x1,
                dy = y2 - y1,
                dr = Math.sqrt(dx * dx + dy * dy),
                drx = dr,
                dry = dr,
                // Change sweep to change orientation of loop.
                sweep = leftHand ? 0 : 1;
            var siblingCount = countSiblingLinks(d.source, d.target)
            var xRotation = 0;
            var largeArc = 0;
            //If a node have more than one link
            if (siblingCount > 1) {
                var siblings = getSiblingLinks(d.source, d.target);
                var arcScale = d3.scale.ordinal()
                    .domain(siblings)
                    .rangePoints([1, siblingCount]);
                //Calcul of link's coordinates
                drx = drx / (1 + (1 / siblingCount) * (arcScale(d.relation.Description) - 1));
                dry = dry / (1 + (1 / siblingCount) * (arcScale(d.relation.Description) - 1));
            }
            // If node is linked with himself
            if (x1 === x2 && y1 === y2) {
                // Fiddle with this angle to get loop oriented.
                xRotation = -45;
                // Needs to be 1.
                largeArc = 1;
                // Make drx and dry different to get an ellipse
                // instead of a circle.
                drx = 30;
                dry = 20;
                // For whatever reason the arc collapses to a point if the beginning
                x2 = x2 + 1;
                y2 = y2 + 1;
            }

            return "M" + x1 + "," + y1 + "A" + drx + ", " + dry + " " + xRotation + ", " + largeArc + ", " + sweep + " " + x2 + "," + y2;
        };

        //Function to detect collisions
        function collide(alpha) {
            var quadtree = d3.geom.quadtree(data.nodes);
            return function(d) {
                var rb = 2 * radius + padding,
                    nx1 = d.x - rb,
                    nx2 = d.x + rb,
                    ny1 = d.y - rb,
                    ny2 = d.y + rb;
                quadtree.visit(function(quad, x1, y1, x2, y2) {
                    if (quad.point && (quad.point !== d)) {
                        var x = d.x - quad.point.x,
                            y = d.y - quad.point.y,
                            l = Math.sqrt(x * x + y * y);
                        if (l < rb) {
                            l = (l - rb) / l * alpha;
                            d.x -= x *= l;
                            d.y -= y *= l;
                            quad.point.x += x;
                            quad.point.y += y;
                        }
                    }
                    return x1 > nx2 || x2 < nx1 || y1 > ny2 || y2 < ny1;
                });
            };
        }
    },
    /**
     * Build nodes and links without locate it, define listener associated to each objects
     *
     * @param vis {vis} g element of SVG constructed
     * @param dataLinks {dataLinks} Array of links data
     * @param dataNodes {dataNodes} Array of nodes data
     * @param mapping {mapping} dictionnary containing index of concept in array and id of concept related
     * @param color {color} Array with color selected
     */
    createNodesandLinks: function(vis, dataLinks, dataNodes, color, mapping) {
        var that = this;
        //Get qxd3
        var d3 = this.__d3Node.getD3();
        //Create all the line without locations
        var path = vis.attr("class", "drawarea")
            .selectAll("path.link")
            .data(dataLinks);
        path.enter().append("path")
            .attr("class", "link")
            .style("fill", "none")
            .style("stroke-width", "2px")
            .on("click", function(d) {
                //Gestion of link click in D3
                //Retrieve information about relation and node involved
                var source = d.source;
                var target = d.target;
                var relation = d.relation;
                //Check if relation is viable
                if (d.relation != null) {
                    that.fireDataEvent("linkClick", getRelationObjectFromLabel(source, target, relation)); //Send data of link to listener
                }
            })
            .each(function(d) {
                //Color links depending on relation label, add marker end with same color
                var color_selected = color(d.relation.Label);
                d3.select(this).style("stroke", color_selected)
                    .attr("marker-end", marker(color_selected));
            });
        path.exit().remove();

        //Invisible link used to build curved links
        var pathInvis = vis.attr("class", "drawarea")
            .selectAll("path.invis")
            .data(dataLinks);
        pathInvis.enter().append("links")
            .attr("class", "invis")
            .style("stroke-width", "0px")
            .style("fill", "none")
        pathInvis.exit().remove();


        //Add nodes to SVG
        var node = vis.attr("class", "drawarea")
            .selectAll(".node")
            .data(dataNodes)
            .enter().append("circle")
            .attr("class", "node")
            .attr("r", 8) //size of circle
            .style("stroke", "black")
            .style("stroke-width", "1.5 px")
            .style("fill", "#91b6d4")
            //Gestion of node click in D3
            .on("click", function(d) {
                if (d.Label != null) {
                    that.fireDataEvent("nodeClick", getIdFromLabel(d.Label, mapping, dataNodes)); //Send data of node to listener
                }
            });

        //Add node's labels
        var label = vis.attr("class", "drawarea")
            .append("g")
            .attr("class", "labels")
            .selectAll("text")
            .data(dataNodes)
            .enter().append("text")
            //.attr('text-anchor', 'middle') // if we want centered text_center
            .attr('dominant-baseline', 'central')
            .style('font-family', 'FontAwesome')
            .style('font-size', '0.8em')
            .attr("dx", +8) //Distonce of label from node
            .attr("dy", ".35em")
            .text(function(d) {
                return d.Label;
            });

        //Create arrow head for all links and fill it with the correct color
        function marker(color) {
            vis.append('defs').append('marker')
                .attr("id", color.replace("#", ""))
                .attr("viewBox", "0 -5 10 10")
                .attr("refX", 15) // This sets how far back it sits
                .attr("refY", 0)
                .attr("markerWidth", 9)
                .attr("markerHeight", 9)
                .attr("orient", "auto")
                .attr("markerUnits", "userSpaceOnUse")
                .append("svg:path")
                .attr("d", "M0,-5L10,0L0,5")
                .style("fill", color);
            return "url(" + color + ")";
        };

        //Function to get ID from Label using mapping object
        function getIdFromLabel(label, mapping, dataNodes) {
            //Loop to find ID from Label
            for (var i = 0; i < dataNodes.length; i++) {
                if (dataNodes[i].Label == label) {
                    var indexLabel = i;
                    for (var i = 0; i < dataNodes.length; i++) {
                        if (dataNodes[i].Label == label) {
                            var indexLabel = i;
                        }
                    }
                }
            }

            //Function to get key from value to determine ID of node clicked
            function getKeyByValue(mapping, indexLabel) {
                return Object.keys(mapping).find(function(key) {
                    return mapping[key] === indexLabel
                });
            }
            var id = getKeyByValue(mapping, indexLabel);
            return id;
        };

        //Function to get triplet from a click on a link
        function getRelationObjectFromLabel(source, target, relation) {
            //Get information from Left node linked by relation clicked
            var left = new elterm.data.Concept();
            left.setId(source.Id);
            left.setLabel(source.Label);
            left.setDescription(source.Description);
            left.setObsolete(source.Obsolete);
            left.setId_terminology(source.IdTerminology);
            left.setName_terminology(source.NameTerminology);
            //Get information from Relation linking left and right node
            var rel = new elterm.data.Relation();
            rel.setId(relation.Id);
            rel.setName(relation.Label);
            rel.setDescription(relation.Description);
            rel.setObsolete(relation.Obsolete);
            //Get information from Right nodes linked by relation clicked
            var right = new elterm.data.Concept();
            right.setId(target.Id);
            right.setLabel(target.Label);
            right.setDescription(target.Description);
            right.setObsolete(target.Obsolete);
            right.setId_terminology(target.IdTerminology);
            right.setName_terminology(target.NameTerminology);
            //Creation of a Triple Object
            var triple = new elterm.data.Triple(left, rel, right);
            return triple;
        };

        return [path, pathInvis, node, label]
    },
    /**
     * Build legend of graph
     *
     * @param svgRoot {svgRoot} Root of SVG constructed
     * @param width {witdh} witdh of SVG constructed
     * @param color {color} Array with color selected
     */
    buildLegend: function(svgRoot, color, width) {
        //Add legend class to SVG and place it
        var legend = svgRoot.selectAll(".legend")
            .data(color.domain())
            .enter().append("g")
            .attr("class", "legend")
            .attr("transform", function(d, i) {
                return "translate(0," + i * 20 + ")";
            });
        //Add it in rectangle
        legend.append("rect")
            .attr("x", width - 18)
            .attr("width", 18)
            .attr("height", 18)
            .style("fill", color);
        //Add text of legend
        legend.append("text")
            .attr("x", width - 24)
            .attr("y", 9)
            .attr("dy", ".15em")
            .style("text-anchor", "end")
            .style("font-size", "0.8em")
            .text(function(d) {
                return d;
            });
    },
    /**
     * Function to check if array contain empty values
     *
     * @param array {array} Array that need to be check for empty values
     */
    hasEmptyElement: function(array) {
        for (var i = 0; i < array.length; i++) {
            if (array[i].source === "") {
                return false;
            }
            if (array[i].target === "") {
                return false;
            }
        }
        return true;
    },
    /**
     * Build button to add new concept or new relation
     *
     * @param svgRoot {svgRoot} Root of SVG constructed
     */
    buildButtons: function(svgRoot) {

        var that = this;
        //Button add concept
        svgRoot //G element of svgRoot
            //add circle in a g element and postion it
            .append("circle") // attach a circle
            .attr("cx", 440) // intial position on x-axis + translation on SVG
            .attr("cy", 287) // position the y-center
            .attr("r", 10) // set the radius
            .attr("fill", "#386890")
            .style('fill-opacity', '1')
            .style("stroke-width", "0.29398149")
            //add listerner on click
            .on('click', function(d) {
                that.fireDataEvent("buttonClick"); //Send true to listener
            });

        svgRoot //Root of SVG
            //add rectangle for plus button and position it
            .append('rect')
            .attr('x', 438) // intial position on x-axis + translation on SVG
            .attr('y', 281)
            .attr('height', 12)
            .attr('width', 4)
            .style('fill', '#ffffff')
            .style('fill-opacity', '1')
            .style('stroke-width', 0.28540233)
            //add listerner on click
            .on('click', function(d) {
                that.fireDataEvent("buttonClick"); //Send true to listener
            });
        svgRoot //Root of SVG
            //add rectangle for plus button and position it
            .append('rect')
            .attr('transform', 'rotate(90)')
            .attr('x', 285)
            .attr('y', -16 - 430) // intial position on x-axis + translation on SVG
            .attr('height', 12)
            .attr('width', 4)
            .style('fill', '#ffffff')
            .style('fill-opacity', '1')
            .style('stroke-width', 0.28540233)
            //add listerner on click
            .on('click', function(d) {
                that.fireDataEvent("buttonClick"); //Send true to listener
            });
        svgRoot //Root of SVG
            //add text of button
            .append("text")
            .attr('dominant-baseline', 'central')
            .style('font-family', 'FontAwesome')
            .style('font-size', '0.8em')
            .attr("dx", -100)
            .attr("x", 440) // intial position on x-axis + translation on SVG
            .attr("y", 287) // position the y-center
            .text("Add Concept");
        //
        // Button add Relation type
        //
        svgRoot //Root of SVG
            //add circle in a g element and postion it, add listener on it
            .append("g")
            .append("circle") // attach a circle
            .attr("cx", 440) // intial position on x-axis + translation on SVG
            .attr("cy", 267) // position the y-center
            .attr("r", 10) // set the radius
            .attr("fill", "#386890")
            .style('fill-opacity', '1')
            .style("stroke-width", "0.29398149")
            .append("text")
            .attr('dominant-baseline', 'central')
            .style('font-family', 'FontAwesome')
            .style('font-size', '0.8em')
            .attr("dx", +15)
            .attr("dy", ".85em")
            .text("Add Relation")
            //add listerner on click
            .on('click', function(d) {
                that.fireDataEvent("buttonRelationClick");
            })
        svgRoot //Root of SVG
            //add rectangle for plus button and position it
            .append('rect')
            .attr('x', 438) // intial position on x-axis + translation on SVG
            .attr('y', 261)
            .attr('height', 12)
            .attr('width', 4)
            .style('fill', '#ffffff')
            .style('fill-opacity', '1')
            .style('stroke-width', 0.28540233)
            //add listerner on click
            .on('click', function(d) {
                that.fireDataEvent("buttonRelationClick"); //Send true to listener
            });
        svgRoot //Root of SVG
            //add rectangle for plus button and position it
            .append('rect')
            .attr('transform', 'rotate(90)')
            .attr('x', 265)
            .attr('y', -16 - 430) // intial position on x-axis + translation on SVG
            .attr('height', 12)
            .attr('width', 4)
            .style('fill', '#ffffff')
            .style('fill-opacity', '1')
            .style('stroke-width', 0.28540233)
            //add listerner on click
            .on('click', function(d) {
                that.fireDataEvent("buttonRelationClick"); //Send true to listener
            });

        svgRoot //Root of SVG
            //add text of button
            .append("text")
            .attr('dominant-baseline', 'central')
            .style('font-family', 'FontAwesome')
            .style('font-size', '0.8em')
            .attr("dx", -100)
            .attr("x", 440) // intial position on x-axis + translation on SVG
            .attr("y", 267) // position the y-center
            .text("Add Relation");
        //
        // Button add link
        //
        svgRoot //Root of SVG
            //add circle in a g element and postion it, add listener on it
            .append("g")
            .append("circle") // attach a circle
            .attr("cx", 440) // intial position on x-axis + translation on SVG
            .attr("cy", 247) // position the y-center
            .attr("r", 10) // set the radius
            .attr("fill", "#386890")
            .style('fill-opacity', '1')
            .style("stroke-width", "0.29398149")
            .append("text")
            .attr('dominant-baseline', 'central')
            .style('font-family', 'FontAwesome')
            .style('font-size', '0.8em')
            .attr("dx", +15)
            .attr("dy", ".85em")
            .text("Add Link")
            //add listerner on click
            .on('click', function(d) {
                that.fireDataEvent("buttonAddLink"); //Send true to listener
            })
        svgRoot //Root of SVG
            //add rectangle for plus button and position it
            .append('rect')
            .attr('x', 438) // intial position on x-axis + translation on SVG
            .attr('y', 241)
            .attr('height', 12)
            .attr('width', 4)
            .style('fill', '#ffffff')
            .style('fill-opacity', '1')
            .style('stroke-width', 0.28540233)
            //add listerner on click
            .on('click', function(d) {
                that.fireDataEvent("buttonAddLink"); //Send true to listener
            });
        svgRoot //Root of SVG
            //add rectangle for plus button and position it
            .append('rect')
            .attr('transform', 'rotate(90)')
            .attr('x', 245)
            .attr('y', -16 - 430) // intial position on x-axis + translation on SVG
            .attr('height', 12)
            .attr('width', 4)
            .style('fill', '#ffffff')
            .style('fill-opacity', '1')
            .style('stroke-width', 0.28540233)
            //add listerner on click
            .on('click', function(d) {
                that.fireDataEvent("buttonAddLink"); //Send true to listener
            });

        svgRoot //Root of SVG
            //add text and position it
            .append("text")
            .attr('dominant-baseline', 'central')
            .style('font-family', 'FontAwesome')
            .style('font-size', '0.8em')
            .attr("dx", -80)
            .attr("x", 440) // intial position on x-axis + translation on SVG
            .attr("y", 247) // position the y-center
            .text("Add Link");
    }
}
});