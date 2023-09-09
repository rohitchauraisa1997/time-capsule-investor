import { useState,useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import Highcharts from 'highcharts/highstock';
import HighchartsExporting from 'highcharts/modules/exporting';
import HighchartsExportData from 'highcharts/modules/export-data';
import axios from 'axios';
HighchartsExporting(Highcharts);
HighchartsExportData(Highcharts);

function StockChart() {
    const location = useLocation();
    const searchParams = new URLSearchParams(location.search);
    const stockCode = searchParams.get('stockCode');
    const stockIndex = searchParams.get('stockIndex');
    const [, setStockData] = useState([]);

    useEffect(() => {
        axios.get(`http://localhost:3000/stock/renderdata?stock_code=${stockCode}&stock_index=${stockIndex}`)
        .then(response => {
            return response.data
        })
        .then(data=>{
            setStockData(data)
            Highcharts.stockChart('container', {
                rangeSelector: {
                    selected: 1
                },
                title: {
                    text: `${stockCode} Stock Price`
                },
                series: [{
                    name: `${stockCode} Stock Price`,
                    data: data,
                    marker: {
                    enabled: true,
                    radius: 3
                    },
                    shadow: true,
                    tooltip: {
                    valueDecimals: 2
                    }
                }]
            }
            )
        }
        )
        .catch(error => {
            console.error('Error fetching data:', error);
        });
    }, []);

    return <div id='container' style={{ height: '400px', minWidth: '310px' }} />
}

export default StockChart;