// Author: Martin Chorley
// LICENSE: MIT
// Source: https://bl.ocks.org/martinjc/7aa53c7bf3e411238ac8aef280bd6581



d3.json("network_graph_data.json", function(error, graph) {
    if (error) throw error;

    var width_from_json = graph.width;
    var height_from_json = graph.height;
    var title_from_json = graph.title;


    var width = window.innerWidth;
    var height = window.innerHeight;
    var svg = d3.select("svg").attr('viewBox', '0 0 ' + width + ' ' + height);


    var simulation = d3.forceSimulation()
        // pull nodes together based on the links between them
        .force("link", d3.forceLink().id(function(d) {
                return d.id;
            })
            .strength(0.025))
        // push nodes apart to space them out
        .force("charge", d3.forceManyBody().strength(-200))
        // add some collision detection so they don't overlap
        .force("collide", d3.forceCollide().radius(12))
        // and draw them around the centre of the SVG
        .force("center", d3.forceCenter(width / 2, height / 2));

    //Add a title recovered from json file
    svg.append("text")
        .attr("x", (width / 2))
        .attr("y", 0 + 35)
        .attr("text-anchor", "middle")
        .style("font-size", "16px")
        .style("text-decoration", "underline")
        .text(title_from_json);
    // Get nodes
    var nodes = graph.nodes;
    // links between nodes
    var links = graph.links;

    // add the curved links to our graphic
    var link = svg.selectAll(".link")
        .data(links)
        .enter()
        .append("path")
        .attr("class", "link")
        .attr('stroke', function(d) {
            return "#009688";
        });

    // add the nodes to the graphic
    var node = svg.selectAll(".node")
        .data(nodes)
        .enter().append("g")

    // a circle to represent the node
    node.append("circle")
        .attr("class", "node")
        .attr("r", 8)
        .attr("fill", "#03a9f4")
        .on("mouseover", mouseOver(.2))
        .on("mouseout", mouseOut)
        .call(d3.drag()
            .on("start", dragstarted)
            .on("drag", dragged)
            .on("end", dragended));

    // hover text for the node
    node.append("title")
        .text(function(d) {
            return d.twitter;
        });

    // add a label to each node
    node.append("text")
        .attr("dx", 12)
        .attr("dy", ".35em")
        .text(function(d) {
            return d.name;
        })
        .style("stroke", "black")
        .style("stroke-width", 0.5)
        .style("fill", function(d) {
            return d.colour;
        });

    // add the nodes to the simulation and
    // tell it what to do on each tick
    simulation
        .nodes(nodes)
        .on("tick", ticked);

    // add the links to the simulation
    simulation
        .force("link")
        .links(links);

    // on each tick, update node and link positions
    function ticked() {
        link.attr("d", positionLink);
        node.attr("transform", positionNode);
    }

    // links are drawn as curved paths between nodes,
    // through the intermediate nodes
    function positionLink(d) {
        var offset = 30;

        var midpoint_x = (d.source.x + d.target.x) / 2;
        var midpoint_y = (d.source.y + d.target.y) / 2;

        var dx = (d.target.x - d.source.x);
        var dy = (d.target.y - d.source.y);

        var normalise = Math.sqrt((dx * dx) + (dy * dy));

        var offSetX = midpoint_x + offset * (dy / normalise);
        var offSetY = midpoint_y - offset * (dx / normalise);

        return "M" + d.source.x + "," + d.source.y +
            "S" + offSetX + "," + offSetY +
            " " + d.target.x + "," + d.target.y;
    }

    // move the node based on forces calculations
    function positionNode(d) {
        // keep the node within the boundaries of the svg
        if (d.x < 0) {
            d.x = 0
        };
        if (d.y < 0) {
            d.y = 0
        };
        if (d.x > width) {
            d.x = width
        };
        if (d.y > height) {
            d.y = height
        };
        return "translate(" + d.x + "," + d.y + ")";
    }

    // build a dictionary of nodes that are linked
    var linkedByIndex = {};
    links.forEach(function(d) {
        linkedByIndex[d.source.index + "," + d.target.index] = 1;
    });

    // check the dictionary to see if nodes are linked
    function isConnected(a, b) {
        return linkedByIndex[a.index + "," + b.index] || linkedByIndex[b.index + "," + a.index] || a.index == b.index;
    }

    // fade nodes on hover
    function mouseOver(opacity) {
        return function(d) {
            // check all other nodes to see if they're connected
            // to this one. if so, keep the opacity at 1, otherwise
            // fade
            node.style("stroke-opacity", function(o) {
                thisOpacity = isConnected(d, o) ? 1 : opacity;
                return thisOpacity;
            });
            node.style("fill-opacity", function(o) {
                thisOpacity = isConnected(d, o) ? 1 : opacity;
                return thisOpacity;
            });
            // also style link accordingly
            link.style("stroke-opacity", function(o) {
                return o.source === d || o.target === d ? 1 : opacity;
            });
            link.style("stroke", function(o) {
                return o.source === d || o.target === d ? o.source.colour : "#ddd";
            });
        };
    }

    function mouseOut() {
        node.style("stroke-opacity", 1);
        node.style("fill-opacity", 1);
        link.style("stroke-opacity", 1);
        link.style("stroke", "#009688");
    }


    var lables = node.append("text")
        .text(function(d) {
            return d.id;
        })
        .attr('x', 6)
        .attr('y', 3);

    node.append("title")
        .text(function(d) {
            return d.id;
        });


    function dragstarted(d) {
        if (!d3.event.active) simulation.alphaTarget(0.3).restart();
        d.fx = d.x;
        d.fy = d.y;
    }

    function dragged(d) {
        d.fx = d3.event.x;
        d.fy = d3.event.y;
    }

    function dragended(d) {
        if (!d3.event.active) simulation.alphaTarget(0);
        d.fx = null;
        d.fy = null;
    }


});