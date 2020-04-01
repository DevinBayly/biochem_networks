<script>

  let distanceTool = 120;
  let off = false;
  let strengthTool = -50;
  let threshold = 2;
  import * as d3 from "d3";
  import {legend} from "./legend.js";
  let width = 5000;
  let height = 5000;
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

  document.querySelector("#legend").append(legend({
  color: d3.scaleSequential([0, max], d3.interpolateViridis),
  title: "Number of shared proteins chunks",
  height:40
}))
    const node = zoom_group
      .append("g")
      .attr("stroke", "#fff")
      .attr("stroke-width", 1.5)
      .selectAll("circle")
      .data(nodes)
      .join("circle")
      .attr("r", d => d.value)
      .attr("fill", "black")
      .call(d3.drag() 
            .on("start", dragstarted) 
            .on("drag", dragged)      
            .on("end", dragended)     
         );
    function dragstarted(d) {
      if (!d3.event.active) simulation.alphaTarget(0.3).restart();//sets the current target alpha to the specified number in the range [0,1].
      d.fy = d.y; //fx - the node’s fixed x-position. Original is null.
      d.fx = d.x; //fy - the node’s fixed y-position. Original is null.
    }

    //When the drag gesture starts, the targeted node is fixed to the pointer
    function dragged(d) {
      d.fx = d3.event.x;
      d.fy = d3.event.y;
    }

    //the targeted node is released when the gesture ends
    function dragended(d) {
      if (!d3.event.active) simulation.alphaTarget(0);
      d.fx = null;
      d.fy = null;
      
      console.log("data after dragged is ...",data);
    }

    zoom_group.append("g").selectAll("text").data(nodes).enter().append("text").text(d => d.id)
    .attr("x",d=> d.x+d.value)
    .attr("y",d=> d.y + d.value)
    .attr("dy",5);

    let ticked = () => {
      link
        .attr("x1", d => d.source.x)
        .attr("y1", d => d.source.y)
        .attr("x2", d => d.target.x)
        .attr("y2", d => d.target.y);

      node
        .attr("cx", d => d.x)
        .attr("cy", d => d.y);

    zoom_group.selectAll("text")
    .attr("x",d=> d.x)
    .attr("y",d=> d.y)
    .attr("dy",5);

    };
    setInterval(() => {
      if (!off ) {
        simulation.tick();
        ticked();
        simulation.alpha(1)
        simulation.restart()
      }
    }, 100);
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
  text {
  text-anchor: middle;
  font-family: "Helvetica Neue", Helvetica, sans-serif;
  fill: #666;
  font-size: 16px;
}
</style>


<div id="holder">

<div id="container" />
<div id="labels">

  <label>
    Min shared protein count
    <input type="number" bind:value={threshold} min="0"  max="7" on:change={restart}/>
    <input type="range" bind:value={threshold} min="0" max="7" on:change={restart}/>
  </label>
  <label>
    Edge Length
    <input type="number" bind:value={distanceTool} min="0" max="3000" />
    <input type="range" bind:value={distanceTool} min="0" max="3000" />
  </label>
  <label>
    Repulsion Strength
    <input type="number" bind:value={strengthTool} min="-10000" max="400" />
    <input type="range" bind:value={strengthTool} min="-10000" max="400" />
  </label>
  <label>
  Stop animation
  <input type="checkbox" bind:checked={off} />
  </label>
</div>
</div>
<div id="legend">
</div>