<script>
  let distanceTool = window.innerHeight / 3;
  let off = false;
  let strengthTool = -509;
  let threshold = 4;
  import * as d3 from "d3";
  let width = window.innerWidth;
  let height = window.innerHeight;
  let max = 0;
  let createGraph = (data, svgArg) => {
    //remove previous
    d3.select("svg").remove()
    let nodes = [];
    let links = [];
    let existingNames = [];

    for (let nodename in data) {

      for (let othernode in data[nodename].edges) {
        //now make as many edges are in the data
        let el = {
          source: nodename,
          target: othernode,
          value: data[nodename].edges[othernode].length
        };
        if (el.value >= threshold){
          links.push(el);
          let node = { id: nodename, value: data[nodename].proteins.length }
          if (existingNames.indexOf(node.id)==-1) {
            nodes.push(node);
            existingNames.push(node.id)
          }
        }
        if (max < el.value) {
          max = el.value;
        }
      }
    }

    const simulation = d3.forceSimulation(nodes);
    console.log(simulation)

    simulation.stop();
    console.log(simulation)
    let forces = simulation
      .force(
        "link",
        d3
          .forceLink(links)
          .id(d => d.id)
          .distance(1000)
      )
      .force("charge", d3.forceManyBody().strength(-509))
      .force("center", d3.forceCenter(width / 2, height / 2));
    const svg = svgArg.attr("viewBox", [0, 0, width, height]);

    console.log(simulation);
    
    const zoom_group = svg.append("g");

    // make a color

    const link = zoom_group
      .append("g")
      .attr("stroke", "#999")
      .attr("stroke-opacity", 0.6)
      .selectAll("line")
      .data(links)
      .join("line")
      .attr("stroke-width", d => d.value)
      .attr("stroke", d => d3.interpolateViridis(d.value / max));

    const node = zoom_group
      .append("g")
      .attr("stroke", "#fff")
      .attr("stroke-width", 1.5)
      .selectAll("circle")
      .data(nodes)
      .join("circle")
      .attr("r", d => d.value)
      .attr("fill", "black");

    node.append("title").text(d => d.id);

    let ticked = () => {
      link
        .attr("x1", d => Math.min(width - 100, Math.abs(d.source.x)))
        .attr("y1", d => Math.min(height - 100, Math.abs(d.source.y)))
        .attr("x2", d => Math.min(width - 100, Math.abs(d.target.x)))
        .attr("y2", d => Math.min(height - 100, Math.abs(d.target.y)));

      node
        .attr("cx", d => Math.min(width - 100, Math.abs(d.x)))
        .attr("cy", d => Math.min(height - 100, Math.abs(d.y)));
    };
    setInterval(() => {
      if (!off ) {
        simulation.tick();
        ticked();
        simulation.alpha(1)
        simulation.restart()
      }
    }, 1000);
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

  let data 
  let svg
  window.onload = async () => {
    data = await fetch("./clean.json").then(res => res.json());
    svg = d3.select("#container").append("svg");
    //let node = createGraph(data, svg);
  };
  let restart =()=> {

    svg = d3.select("#container").append("svg");
    createGraph(data,svg)
  }
</script>

<style>
  #holder {
      display:flex;
  }
</style>


<div id="holder">

<div id="container" />
<div id="labels">

  <label>
    <input type="number" bind:value={distanceTool} min="0" max="3000" />
    <input type="range" bind:value={distanceTool} min="0" max="3000" />
  </label>
  <label>
    <input type="number" bind:value={threshold} min="0" {max} on:change={restart}/>
    <input type="range" bind:value={threshold} min="0" {max} on:change={restart}/>
  </label>

  <label>
    <input type="number" bind:value={strengthTool} min="-10000" max="-30" />
    <input type="range" bind:value={strengthTool} min="-10000" max="-30" />
  </label>
  <input type="checkbox" bind:checked={off} />
</div>
</div>
