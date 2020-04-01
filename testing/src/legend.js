import * as d3 from "d3"

export function colorCanvas (){
    let can = document.querySelector("canvas")
    can.height=100
    can.width= document.querySelector("#container").getBoundingClientRect().width
    let ctx = can.getContext("2d")
    let color = d3.interpolateViridis
    let textheight = 75
    for (let i = 0;i < can.width-1;i++) {
        ctx.fillStyle=color(i/can.width)
        ctx.fillRect(i,0,i+1,can.height-textheight)
    }
    // notes
    let num = Math.floor(can.width/7)
    ctx.fillStyle="black"
    for (let i = 0;i< 7;i++) {
        ctx.font="15px Arial"
        ctx.fillText(i,10+num*i,can.height-(textheight/2))
    }
}