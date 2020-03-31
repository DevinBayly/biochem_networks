<script>
  import * as d3 from "d3";
  let width = 10000;
  let height = 10000;
  let makeGraph = data => {
    let nodes = [];
    let links = [];
    for (let nodename in data) {
      nodes.push({ id: nodename });
      for (let othernode in data[nodename].edges) {
        links.push({ source: nodename, target: othernode, value: 2 });
      }
    }
    console.log(nodes);
    console.log(links);
  };
  let createGraph = (data, svgArg) => {
    let nodes = [];
    let links = [];
    for (let nodename in data) {
      nodes.push({ id: nodename });
      for (let othernode in data[nodename].edges) {
        links.push({ source: nodename, target: othernode, value: 2 });
      }
    }

    const simulation = d3
      .forceSimulation(nodes)
      .force("link", d3.forceLink(links).id(d => d.id))
      .force("charge", d3.forceManyBody())
      .force("center", d3.forceCenter(width / 2, height / 2));

    const svg = svgArg.attr("viewBox", [0, 0, width, height]);

    const zoom_group = svg.append("g")

    const link = zoom_group
      .append("g")
      .attr("stroke", "#999")
      .attr("stroke-opacity", 0.6)
      .selectAll("line")
      .data(links)
      .join("line")
      .attr("stroke-width", d => Math.sqrt(d.value));

    const node = zoom_group
      .append("g")
      .attr("stroke", "#fff")
      .attr("stroke-width", 1.5)
      .selectAll("circle")
      .data(nodes)
      .join("circle")
      .attr("r", 5)
      .attr("fill", "black");

    node.append("title").text(d => d.id);

    simulation.on("tick", () => {
      link
        .attr("x1", d => d.source.x)
        .attr("y1", d => d.source.y)
        .attr("x2", d => d.target.x)
        .attr("y2", d => d.target.y);

      node.attr("cx", d => d.x).attr("cy", d => d.y);
    });

    svg.call(
      d3
        .zoom()
        .extent([[0, 0], [width, height]])
        .scaleExtent([1, 8])
        .on("zoom", zoomed)
    );

    function zoomed() {
      zoom_group.attr("transform", d3.event.transform);
    }

    return svg;
  };

  window.onload = async () => {
    let data = await fetch("./bio.json").then(res => res.json());
    let svg = d3.select("#container").append("svg");
    let node = createGraph(data, svg);
  };
</script>

<div id="container" />
