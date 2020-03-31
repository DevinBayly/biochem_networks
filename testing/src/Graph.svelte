<script>
  let distanceTool = 1000;
  let strengthTool = -509;
  import * as d3 from "d3";
  let width = 3000;
  let height = 3000;
  let max = 0;
  let createGraph = (data, svgArg) => {
    let nodes = [];
    let links = [];
    let existingNames = [];
    for (let name in data) {
      existingNames.push(name);
    }

    for (let nodename in data) {
      nodes.push({ id: nodename, value: data[nodename].proteins.length });

      for (let othernode in data[nodename].edges) {
        //now make as many edges are in the data
        if (existingNames.indexOf(othernode) == -1) {
          nodes.push({ id: othernode, value: 1 });
        }
        let el = {
          source: nodename,
          target: othernode,
          value: data[nodename].edges[othernode].length
        };
        links.push(el);
        if (max < el.value) {
          max = el.value;
        }
      }
    }

    const simulation = d3
      .forceSimulation(nodes)
      .force(
        "link",
        d3
          .forceLink(links)
          .id(d => d.id)
          .distance(1000)
      )
      .force("charge", d3.forceManyBody().strength(-509))
      .force("center", d3.forceCenter(width / 2, height / 2))
      .alphaTarget(1);

    const svg = svgArg.attr("viewBox", [0, 0, width, height]);

    const zoom_group = svg.append("g");

    // make a color

    const link = zoom_group
      .append("g")
      .attr("stroke", "#999")
      .attr("stroke-opacity", 0.6)
      .selectAll("line")
      .data(links)
      .join("line")
      .attr("stroke-width", d => d.value * 5)
      .attr("color", d => d3.interpolateReds(d.value / max));

    const node = zoom_group
      .append("g")
      .attr("stroke", "#fff")
      .attr("stroke-width", 1.5)
      .selectAll("circle")
      .data(nodes)
      .join("circle")
      .attr("r", d => d.value * 5)
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
    d3.interval(() => {
      simulation
        .nodes(nodes)
        .force("link", d3.forceLink(links).distance(distanceTool))
        .force("center", d3.forceCenter(width / 2, height / 2))
        .force("charge", d3.forceManyBody().strength(strengthTool));
    }, 2000);
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
    let data = await fetch("./subtest.json").then(res => res.json());
    let svg = d3.select("#container").append("svg");
    let node = createGraph(data, svg);
  };
</script>

<label>
  <input type="number" bind:value={distanceTool} min="0" max="3000" />
  <input type="range" bind:value={distanceTool} min="0" max="3000" />
</label>
<label>
  <input type="number" bind:value={strengthTool} min="-1000" max="-30" />
  <input type="range" bind:value={strengthTool} min="-1000" max="-30" />
</label>

<div id="container" />
