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

    const width = 500;
    const height = 300;
    const margin = { top: 20, right: 30, bottom: 40, left: 40 };

    // Ensure all values are numbers (already ensured by type)
    const numericValues = Object.values(data);

    const minValue = d3.min(numericValues) || 0;
    const maxValue = d3.max(numericValues) || 1;

    const x = d3.scaleBand<string>()
        .domain(Object.keys(data))
        .range([margin.left, width - margin.right])
        .padding(0.1);

    // Adjust the y-scale to accommodate negative values
    const y = d3.scaleLinear()
        .domain([minValue, maxValue])  // Allows for negative values
        .nice()
        .range([height - margin.bottom, margin.top]);

    const svg = d3.select('#chart')
        .append('svg')
        .attr('width', width)
        .attr('height', height);

    // Define the zero position (baseline)
    const zeroY = y(0);

    // Create a group for each bar (rect and text)
    const barGroup = svg.append('g')
        .selectAll<SVGGElement, [string, number]>('g')
        .data(Object.entries(data))
        .enter()
        .append('g')
        .attr('transform', d => `translate(${x(d[0])}, 0)`);

    // Append rectangles (bars)
    barGroup.append('rect')
        .attr('x', 0)
        .attr('y', d => {
            const value = d[1];
            return value >= 0 ? y(value) : zeroY;
        })
        .attr('width', x.bandwidth())
        .attr('height', d => {
            const value = d[1];
            return Math.abs(y(value) - y(0));
        })
        .attr('fill', d => d[1] >= 0 ? 'steelblue' : 'crimson');

    // Append text labels
    barGroup.append('text')
        .attr('x', x.bandwidth() / 2)
        .attr('y', d => {
            const value = d[1];
            if (value >= 0) {
                // For positive values, place text above the bar
                return y(value) - 5;
            } else {
                // For negative values, place text below the bar
                return y(value) + Math.abs(y(value) - y(0)) + 15;
            }
        })
        .attr('text-anchor', 'middle')
        .attr('font-size', '12px')
        .attr('fill', 'black')
        .text(d => d[1].toFixed(4));  // Display the sentiment score with 4 decimal places

    // Add x-axis
    svg.append('g')
        .attr('transform', `translate(0,${zeroY})`)
        .call(d3.axisBottom(x));

    // Add y-axis
    svg.append('g')
        .attr('transform', `translate(${margin.left},0)`)
        .call(d3.axisLeft(y));

    // Add a line at y=0
    svg.append('line')
        .attr('x1', margin.left)
        .attr('x2', width - margin.right)
        .attr('y1', zeroY)
        .attr('y2', zeroY)
        .attr('stroke', 'black');
}

// Create the bar chart
createBarChart();
