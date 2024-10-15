import * as d3 from 'd3';

type StockData = { [ticker: string]: number };

async function getStockData(): Promise<StockData> {
    const response = await fetch('http://127.0.0.1:8000/api/stock-sentiment/');
    if (response.ok) {
        const stockData: StockData = await response.json();
        return stockData;
    } else {
        console.error("Failed to get stock data");
        return {};
    }
}

async function createBarChart() {
    const data: StockData = await getStockData();
    if (!data || Object.keys(data).length === 0) {
        console.error('No valid data to display');
        return;
    }

    const width = 800;
    const height = 500;
    const margin = { top: 60, right: 40, bottom: 80, left: 70 };

    // Extract numerical values from data
    const numericValues = Object.values(data);

    const minValue = d3.min(numericValues) || 0;
    const maxValue = d3.max(numericValues) || 1;

    const x = d3.scaleBand<string>()
        .domain(Object.keys(data))
        .range([margin.left, width - margin.right])
        .padding(0.2);

    if (Object.keys(data).length === 1) {
        x.range([width / 2 - 50, width / 2 + 50]); // Ensure bar has decent width
    }

    // Adjust the y-scale to accommodate negative values
    const y = d3.scaleLinear()
        .domain([minValue > 0 ? 0 : minValue, maxValue])
        .nice()
        .range([height - margin.bottom, margin.top]);

    const svg = d3.select('#chart')
        .html('') // Clear any existing content
        .append('svg')
        .attr('width', width)
        .attr('height', height);

    // Define the zero position (baseline)
    const zeroY = y(0);

    // Create a group for the bars
    const barGroup = svg.append('g');

    // Append rectangles (bars)
    const bars = barGroup.selectAll('rect')
        .data(Object.entries(data))
        .enter()
        .append('rect')
        .attr('x', d => x(d[0])!)
        .attr('y', d => {
            const value = d[1];
            return value >= 0 ? y(value) : zeroY;
        })
        .attr('width', x.bandwidth())
        .attr('height', d => Math.abs(y(d[1]) - y(0)))
        .attr('fill', d => d[1] >= 0 ? 'green' : 'crimson')
        .attr('opacity', 0.8);

    // Add tooltips on hover
    const tooltip = d3.select('#chart').append('div')
        .attr('class', 'tooltip')
        .style('display', 'none');

    bars.on('mouseover', function (event, d) {
        d3.select(this).attr('opacity', 1);
        tooltip.style('display', 'inline-block')
            .html(`<strong>${d[0]}</strong><br>Sentiment Score: ${d[1].toFixed(4)}`);
    })
        .on('mousemove', function (event) {
            tooltip.style('left', event.pageX + 15 + 'px')
                .style('top', event.pageY - 35 + 'px');
        })
        .on('mouseout', function () {
            d3.select(this).attr('opacity', 0.8);
            tooltip.style('display', 'none');
        });

    // Add x-axis
    svg.append('g')
        .attr('transform', `translate(0,${zeroY})`)
        .call(d3.axisBottom(x))
        .selectAll('text')
        .attr('transform', 'rotate(-45)')
        .attr('text-anchor', 'end')
        .attr('dx', '-0.6em')
        .attr('dy', '0.15em');

    // Add y-axis
    svg.append('g')
        .attr('transform', `translate(${margin.left},0)`)
        .call(d3.axisLeft(y));

    // Add x-axis label
    svg.append('text')
        .attr('x', width / 2)
        .attr('y', height - margin.bottom / 3)
        .attr('text-anchor', 'middle')
        .attr('font-size', '16px')
        .text('Stock Ticker');

    // Add y-axis label
    svg.append('text')
        .attr('transform', 'rotate(-90)')
        .attr('x', -height / 2)
        .attr('y', margin.left / 3)
        .attr('text-anchor', 'middle')
        .attr('font-size', '16px')
        .text('Sentiment Score');

    // Add chart title
    svg.append('text')
        .attr('x', width / 2)
        .attr('y', margin.top / 2)
        .attr('text-anchor', 'middle')
        .attr('font-size', '22px')
        .attr('font-weight', 'bold')
        .text('Stock Sentiment Analysis');

    // Add a line at y=0
    svg.append('line')
        .attr('x1', margin.left)
        .attr('x2', width - margin.right)
        .attr('y1', zeroY)
        .attr('y2', zeroY)
        .attr('stroke', '#333');

    // Add gridlines
    svg.append('g')
        .attr('class', 'grid')
        .attr('transform', `translate(${margin.left},0)`)
        .call((g) => {
            g.call(
                d3.axisLeft(y)
                    .ticks(10)
                    .tickSize(-width + margin.left + margin.right)
                    .tickFormat(() => '')
            );
        });

}

// Create the bar chart
createBarChart();
