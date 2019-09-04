
function generate_pie(data)
{
    pie_content = [];
    console.log(data);
    pcolor = {}
    $.each(data, function(key, value)
    {
        if (colorsjson[key]){
            pcolor[key] = colorsjson[key];
            console.log(key);
        }
        else
            pcolor[key] = generate_color();
            pie_content.push(
            {
                label:key,
                value: data[key],
                color: pcolor[key],
                caption: `${key} - ${data[key]} mins`
            }
        )
    });

    console.log(pie_content);
    pie = new d3pie("pieChart", {
        "header": {
            
            "titleSubtitlePadding": 9
        },
        "footer": {
            "color": "#999999",
            "fontSize": 10,
            "font": "open sans",
            "location": "bottom-left"
        },
        "size": {
            "canvasWidth": 590,
            "pieOuterRadius": "90%",
            "pieInnerRadius": "50%"
        },
        "data": {
            "sortOrder": "value-desc",
            "content": pie_content
        },
        "labels": {
            "outer": {
                "pieDistance": 32
            },
            "inner": {
                "hideWhenLessThanPercentage": 3
            },
            "mainLabel": {
                "fontSize": 14
            },
            "percentage": {
                "color": "#ffffff",
                "decimalPlaces": 2
            },
            "value": {
                "color": "#adadad",
                "fontSize": 14
            },
            "lines": {
                "enabled": true
            },
            "truncation": {
                "enabled": true
            }
        },
        "tooltips": {
            "enabled": true,
            "type": "caption",
            // "string": "{label}: {value} mins, {percentage}%",
            "styles": {
                "fadeInSpeed": 387,
                "backgroundOpacity": 0.68,
                "fontSize": 14,
                "padding": 14
            }
        },
        "effects": {
            "pullOutSegmentOnClick": {
                "speed": 100,
                "size": 14
            }
        },
        "misc": {
            "gradient": {
                "enabled": true,
                "percentage": 100
            }
        }
    });
}

$(document).ready(function(){
    processcount = {};
    colorsjson = {};
    colorsloaded = false;
    buildvisuals();
//console.log(processcount);

    
});

async function buildvisuals()
{
    try{
    colorsjson = await d3.json("colors.json");
    colorsloaded = true;
    }
    catch{

    }

    
    d3.csv("watch4.csv").then(function(data) {
        console.log(data);
        processed_data = []
        data.forEach(function(row)
        {
            if(processcount[row.process])
                processcount[row.process] = (processcount[row.process]+1);
            else
                processcount[row.process] = 1;
            var date = new Date(row.Date);
            processed_data.push({
                title: row.title,
                process: row.process,
                date: date,
                group: date.getMinutes(),
                variable: date.getHours()
            });
        });
        
        console.log(processcount);

        generate_pie(processcount);
        console.log(processed_data);
        buildHeatMap(processed_data);
        loadnumeric();
    
    });

}

function generate_color()
{
    var hexstr = '#';
    for(var i = 0 ; i< 6; i++)
        hexstr+=getRandomArbitrary(0, 15).toString(16);

    return hexstr;
}

function getRandomArbitrary(min, max) {
    return Math.round(Math.random() * (max - min) + min);
}

function buildHeatMap(csv_data)
{
    var margin = {top: 80, right: 25, bottom: 30, left: 40},
    width = 1200 - margin.left - margin.right,
    height = 450 - margin.top - margin.bottom;

    // append the svg object to the body of the page
    var svg = d3.select("#my_dataviz")
    .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform",
            "translate(" + margin.left + "," + margin.top + ")");

  
        var myGroups = [];
        for(var i = 0; i<60; i++)
            myGroups.push(i.toString());
        
        var myVars = [];
        for(var i = 23; i>=0; i--)
            myVars.push(i.toString());

        // Build X scales and axis:
        var x = d3.scaleBand()
            .range([ 0, width ])
            .domain(myGroups)
            .padding(0.05);
        svg.append("g")
            .style("font-size", 15)
            .attr("transform", "translate(0," + height + ")")
            .call(d3.axisBottom(x).tickSize(0))
            .select(".domain").remove()

        // Build Y scales and axis:
        var y = d3.scaleBand()
            .range([ height, 0 ])
            .domain(myVars)
            .padding(0.05);
        svg.append("g")
            .style("font-size", 15)
            .call(d3.axisLeft(y).tickSize(0))
            .select(".domain").remove()

        // // Build color scale
        // var myColor = d3.scaleSequential()
        //     .interpolator(d3.interpolateInferno)
        //     .domain([1,100])

        // create a tooltip
        var tooltip = d3.select("#my_dataviz")
            .append("div")
            .style("opacity", 0)
            .attr("class", "tooltip")
            .style("background-color", "rgba(0, 0, 0, 0.8)")
            .style("color", "white")
            .style("width", "auto")
            .style("border", "solid")
            .style("position", "absolute")
            .style("border-width", "0px")
            .style("border-radius", "0px")
            .style("box-shadow", "1px 1px 3px rgba(0, 0, 0, 0.5)")
            .style("padding", "5px")

        // Three function that change the tooltip when user hover / move / leave a cell
        var mouseover = function(d) {
            tooltip
            .style("opacity", 1)
            d3.select(this)
            .style("stroke", "black")
            .style("opacity", 1)
        }
        var mousemove = function(d) {
            
            tooltip
            .style("display", "block");
            tooltip
            .html(`${d.process}<br/>${d.title}<br/><small>${d.date}</small>`)
            .style("left", (d3.mouse(this)[0]+50) + "px")
            .style("top", (d3.mouse(this)[1]+0) + "px")
        }
        var mouseleave = function(d) {
            tooltip
            .style("opacity", 0)
            d3.select(this)
            .style("stroke", "none")
            .style("opacity", 0.8)

            tooltip
            .style("display", "none");
        }

        // add the squares
        console.log(csv_data);
        svg.selectAll()
            .data(csv_data, function(d) {return d.group+':'+d.variable;})
            .enter()
            .append("rect")
            .attr("x", function(d) { return x(d.group) })
            .attr("y", function(d) { return y(d.variable) })
            .attr("rx", 1)
            .attr("ry", 1)
            .attr("width", x.bandwidth() )
            .attr("height", y.bandwidth() )
            .style("fill", function(d) { return pcolor[d.process];} )
            .style("stroke-width", 1)
            .style("stroke", "none")
            .style("opacity", 0.8)
            .on("mouseover", mouseover)
            .on("mousemove", mousemove)
            .on("mouseleave", mouseleave)
    // });

    // Add title to graph
    svg.append("text")
            .attr("x", 0)
            .attr("y", -50)
            .attr("text-anchor", "left")
            .style("font-size", "22px")
            .text("Activity");

    // Add subtitle to graph
    svg.append("text")
            .attr("x", 0)
            .attr("y", -20)
            .attr("text-anchor", "left")
            .style("font-size", "14px")
            .style("fill", "grey")
            .style("max-width", 400)
            .text("Minute-to-Minute activity map");

}

function loadnumeric()
{
    console.log(pie_content);
    var $numeric = $('#numeric table');
    pie_content.sort(function(a, b)
    {
        return b.value - a.value;
    })
    pie_content.forEach(function(proc){
        
        $numeric.append(
            `
                <tr>
                <td>${proc.label} <span style="background:${proc.color}; width:10px; padding-left:5px; padding-right:5px;">&nbsp;</span></td>
                <td>${formattime(proc.value)}</td>
                </tr>
            `
        )
    });
}

function formattime(value)
{
    return `${Math.round(value/60)} hr ${value % 60} min`;
}
