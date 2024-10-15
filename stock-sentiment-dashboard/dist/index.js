var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __generator = (this && this.__generator) || function (thisArg, body) {
    var _ = { label: 0, sent: function() { if (t[0] & 1) throw t[1]; return t[1]; }, trys: [], ops: [] }, f, y, t, g = Object.create((typeof Iterator === "function" ? Iterator : Object).prototype);
    return g.next = verb(0), g["throw"] = verb(1), g["return"] = verb(2), typeof Symbol === "function" && (g[Symbol.iterator] = function() { return this; }), g;
    function verb(n) { return function (v) { return step([n, v]); }; }
    function step(op) {
        if (f) throw new TypeError("Generator is already executing.");
        while (g && (g = 0, op[0] && (_ = 0)), _) try {
            if (f = 1, y && (t = op[0] & 2 ? y["return"] : op[0] ? y["throw"] || ((t = y["return"]) && t.call(y), 0) : y.next) && !(t = t.call(y, op[1])).done) return t;
            if (y = 0, t) op = [op[0] & 2, t.value];
            switch (op[0]) {
                case 0: case 1: t = op; break;
                case 4: _.label++; return { value: op[1], done: false };
                case 5: _.label++; y = op[1]; op = [0]; continue;
                case 7: op = _.ops.pop(); _.trys.pop(); continue;
                default:
                    if (!(t = _.trys, t = t.length > 0 && t[t.length - 1]) && (op[0] === 6 || op[0] === 2)) { _ = 0; continue; }
                    if (op[0] === 3 && (!t || (op[1] > t[0] && op[1] < t[3]))) { _.label = op[1]; break; }
                    if (op[0] === 6 && _.label < t[1]) { _.label = t[1]; t = op; break; }
                    if (t && _.label < t[2]) { _.label = t[2]; _.ops.push(op); break; }
                    if (t[2]) _.ops.pop();
                    _.trys.pop(); continue;
            }
            op = body.call(thisArg, _);
        } catch (e) { op = [6, e]; y = 0; } finally { f = t = 0; }
        if (op[0] & 5) throw op[1]; return { value: op[0] ? op[1] : void 0, done: true };
    }
};
import * as d3 from 'd3';
function getStockData() {
    return __awaiter(this, void 0, void 0, function () {
        var response, stockData;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0: return [4 /*yield*/, fetch('http://127.0.0.1:8000/api/stock-sentiment/')];
                case 1:
                    response = _a.sent();
                    if (!response.ok) return [3 /*break*/, 3];
                    return [4 /*yield*/, response.json()];
                case 2:
                    stockData = _a.sent();
                    return [2 /*return*/, stockData];
                case 3:
                    console.error("Failed to get stock data");
                    return [2 /*return*/, {}];
            }
        });
    });
}
function createBarChart() {
    return __awaiter(this, void 0, void 0, function () {
        var data, width, height, margin, numericValues, minValue, maxValue, x, y, svg, zeroY, barGroup;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0: return [4 /*yield*/, getStockData()];
                case 1:
                    data = _a.sent();
                    if (!data || Object.keys(data).length === 0) {
                        console.error('No valid data to display');
                        return [2 /*return*/];
                    }
                    width = 500;
                    height = 300;
                    margin = { top: 20, right: 30, bottom: 40, left: 40 };
                    numericValues = Object.values(data);
                    minValue = d3.min(numericValues) || 0;
                    maxValue = d3.max(numericValues) || 1;
                    x = d3.scaleBand()
                        .domain(Object.keys(data))
                        .range([margin.left, width - margin.right])
                        .padding(0.1);
                    y = d3.scaleLinear()
                        .domain([minValue, maxValue]) // Allows for negative values
                        .nice()
                        .range([height - margin.bottom, margin.top]);
                    svg = d3.select('#chart')
                        .append('svg')
                        .attr('width', width)
                        .attr('height', height);
                    zeroY = y(0);
                    barGroup = svg.append('g')
                        .selectAll('g')
                        .data(Object.entries(data))
                        .enter()
                        .append('g')
                        .attr('transform', function (d) { return "translate(".concat(x(d[0]), ", 0)"); });
                    // Append rectangles (bars)
                    barGroup.append('rect')
                        .attr('x', 0)
                        .attr('y', function (d) {
                        var value = d[1];
                        return value >= 0 ? y(value) : zeroY;
                    })
                        .attr('width', x.bandwidth())
                        .attr('height', function (d) {
                        var value = d[1];
                        return Math.abs(y(value) - y(0));
                    })
                        .attr('fill', function (d) { return d[1] >= 0 ? 'steelblue' : 'crimson'; });
                    // Append text labels
                    barGroup.append('text')
                        .attr('x', x.bandwidth() / 2)
                        .attr('y', function (d) {
                        var value = d[1];
                        if (value >= 0) {
                            // For positive values, place text above the bar
                            return y(value) - 5;
                        }
                        else {
                            // For negative values, place text below the bar
                            return y(value) + Math.abs(y(value) - y(0)) + 15;
                        }
                    })
                        .attr('text-anchor', 'middle')
                        .attr('font-size', '12px')
                        .attr('fill', 'black')
                        .text(function (d) { return d[1].toFixed(4); }); // Display the sentiment score with 4 decimal places
                    // Add x-axis
                    svg.append('g')
                        .attr('transform', "translate(0,".concat(zeroY, ")"))
                        .call(d3.axisBottom(x));
                    // Add y-axis
                    svg.append('g')
                        .attr('transform', "translate(".concat(margin.left, ",0)"))
                        .call(d3.axisLeft(y));
                    // Add a line at y=0
                    svg.append('line')
                        .attr('x1', margin.left)
                        .attr('x2', width - margin.right)
                        .attr('y1', zeroY)
                        .attr('y2', zeroY)
                        .attr('stroke', 'black');
                    return [2 /*return*/];
            }
        });
    });
}
// Create the bar chart
createBarChart();
