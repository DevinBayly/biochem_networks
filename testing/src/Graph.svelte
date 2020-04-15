<script>
  let distanceTool = 120;
  let off = false;
  let strengthTool = -50;
  let threshold = 5;
  import * as d3 from "d3";
  import legend from "d3-svg-legend"
  let width = 7000 ;
  let height = 7000;
  let max = 0;
  let createGraph = (data, svgArg) => {
    //remove previous
    d3.select("svg").remove();
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
        if (el.value > max) {
          max = el.value
        }
        if (el.value >= threshold) {
          links.push(el);
          let node = {
            id: nodename,
            value: data[nodename]["category_value"]
          };
          if (existingNames.indexOf(node.id) == -1) {
            nodes.push(node);
            existingNames.push(node.id);
          }
        }
      }
    }

    const simulation = d3.forceSimulation(nodes);
    console.log(simulation);

    simulation.stop();
    console.log(simulation);
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
    svg.attr("height", height / 10);
    svg.attr("width", width / 10);

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
      .attr("stroke-width", d => d.value*4)
      .attr("stroke", d => d3.interpolateViridis((d.value - threshold)/(max-threshold)));
    // make a binning for the values of the nodes
    let minMaxVal;
    let radiiRange = [50,250]
    {
      let vals = nodes.map(e => e.value);
      minMaxVal = [Math.min(...vals), Math.max(...vals)];
    }

    const sizeScale = d3.scaleLinear(minMaxVal,radiiRange)
    const node = zoom_group
      .append("g")
      .selectAll("circle")
      .data(nodes)
      .join("circle")
      .attr("stroke-width", 3.5)
      .attr("r", d => sizeScale(d.value))
      .attr("fill-opacity",.5)
      .call(
        d3
          .drag()
          .on("start", dragstarted)
          .on("drag", dragged)
          .on("end", dragended)
      );
    // create size legend for nodes

    let offsets = radiiRange[1]+50
    svg
      .append("g")
      .attr("class", "legendSize")
      .attr("transform", "translate("+150+","+offsets+")");
    var legendSize = legend.legendSize().scale(sizeScale)
      .shape("circle")
      .shapePadding(offsets)
      .labelOffset(offsets)
      .orient("horizontal")
      .title("Category size using sum total of unique proteins");


    svg.select(".legendSize").call(legendSize);
    // now the edge legend, put at the bottom
          
var viridisScale = d3.scaleSequential(d3.interpolateViridis)
  .domain([threshold,max])


svg.append("g")
  .attr("class", "legendViridis")
  .attr("transform", `translate(${30},${1300})`);

var legendViridis = legend.legendColor()
    .shapeWidth(width/(4*(max-threshold +1)))
    .shapeHeight(200)
    .cells(max-threshold + 1)
    .labelOffset(180)
    .orient("horizontal")
    .scale(viridisScale) 
    .title("Number of shared unique Proteins")

svg.select(".legendViridis")
  .call(legendViridis);
          
        
    function dragstarted(d) {
      if (!d3.event.active) simulation.alphaTarget(0.3).restart(); //sets the current target alpha to the specified number in the range [0,1].
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
      d.fx = d3.event.x;
      d.fy = d3.event.y;
      d.moused = true;
      console.log("data after dragged is ...", data);
    }

    zoom_group
      .append("g")
      .selectAll("text")
      .data(nodes)
      .enter()
      .append("text")
      .text(d => d.id.replace(/hsa.*? /, ""))
      .attr("x", d => d.x + sizeScale(d.value) +200)
      .attr("y", d => d.y + sizeScale(d.value) +200)
      .attr("dy", 5);

    let ticked = () => {
      link
        .attr("x1", d => d.source.x)
        .attr("y1", d => d.source.y)
        .attr("x2", d => d.target.x)
        .attr("y2", d => d.target.y);

      node.attr("cx", d => d.x).attr("cy", d => d.y);

      zoom_group
        .selectAll("text")

        .attr("x", d => d.x + (Math.floor(d.value / 40) + 1) * 5)
        .attr("y", d => d.y + (Math.floor(d.value / 40) + 1) * 5)
        .attr("dy", 5);
    };
    let prevIter;
    setInterval(() => {
      if (off) {
        nodes.map(node => {
          node.fx = node.x;
          node.fy = node.y;
        });
        prevIter = off;
      }
      if (!off && prevIter) {
        // go through and change all the not mouse spec ones back to non fx
        nodes.map(node => {
          if (!node.moused) {
            node.fx = null;
            node.fy = null;
          }
        });
      }
      simulation.tick();
      ticked();
      simulation.alpha(1);
      simulation.restart();
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

  let data;
  let svg;

  let restart = () => {
    svg = d3.select("#container").append("svg");
    createGraph(data, svg);

  };
  window.onload = async () => {
    data = await fetch("./total_counts_version.json").then(res => res.json());
    svg = d3.select("#container").append("svg");
    //let node = createGraph(data, svg);
    let download = document.querySelector("#download");
    download.onclick = () => {
      let a = document.createElement("a");
      a.href = URL.createObjectURL(
        new Blob([document.querySelector("svg").outerHTML])
      );
      a.download = "ProteinNetwork.svg";
      a.click();
    };
    restart();
  };
  // download button code
</script>

<style>
  #holder {
    display: flex;
  }
  text {
    text-anchor: middle;
    font-family: "Helvetica Neue", Helvetica, sans-serif;
    fill: #666;
    font-size: 100px;
  }
</style>

<div id="holder">

  <div id="container" />
  <div id="labels">

    <label>
      Min shared protein count
      <input
        type="number"
        bind:value={threshold}
        min="0"
        max="7"
        on:change={restart} />
      <input
        type="range"
        bind:value={threshold}
        min="0"
        max="7"
        on:change={restart} />
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
    <button id="download">Download svg</button>
  </div>
</div>
