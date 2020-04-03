<script>
  import Graph from "./Graph.svelte";
  export let name;
</script>

<style>
  img {
    width: 20%;
  }
</style>

<a href="http://rtdv-intake.glitch.me/">
  <img src="rtdvicon.png" alt="" />
</a>
<h1>Biochem Networks</h1>
<p>
  This project was produced to assist a UArizona Biochemistry PhD candidate
  <a href="https://cbc.arizona.edu/directory/people/brittany-stankavich">Brittany Stankavich</a> with her understanding of the relationships between
  certain protein categories and their components
</p>
<Graph />
