import {useEffect, useState } from 'react';
import {
  TextField,
  FormControl,
  InputLabel,
  MenuItem,
  Select,
  Button,
  Container,
  Grid,
  Chip
} from '@mui/material';
import axios from 'axios';
import {useNavigate,useLocation} from "react-router-dom";
import CircularProgress from '@mui/material/CircularProgress';
import './App.css'
import Slider from '@mui/material/Slider';
import Box from '@mui/material/Box';
import { Typography } from '@mui/material';
const UpdateBucket = () => {
    const navigate = useNavigate()

    const [bucketName, setBucketName] = useState('');
    const [bucketPeriod, setBucketPeriod] = useState(0);
    const [bucketInvestment, setBucketInvestment] = useState('');
    const [allStocksList, setAllStocksList] = useState([])
    const [selectedStocks, setSelectedStocks] = useState([]);

    // loading symbol
    const [loading, setLoading] = useState(false);


    const location = useLocation();
    const searchParams = new URLSearchParams(location.search);
    const id = searchParams.get('id');
    const stockIndex = searchParams.get('stockIndex');

    const bucketgetUrl = `http://localhost:3000/bucket/?id=${id}&stock_index=${stockIndex}`

    useEffect(() => {
        axios.get(`http://localhost:3000/stock/list?stock_index=${stockIndex}`, {
            headers: {
            Authorization: "Bearer " + localStorage.getItem("token")
            }
        })
        .then(response => {
        return response.data; 
        })
        .then(data => {
            var stocksList = data
            const concatenatedArray = stocksList.map((subArray) => subArray.join('=>'));
            setAllStocksList(concatenatedArray);
        })
        .catch(error => {
        // Handle any errors that occur during the request.
            console.error("Error fetching data:", error);
        });
    }, []);



    useEffect(() => {
        axios.get(bucketgetUrl, {
            headers: {
            Authorization: "Bearer " + localStorage.getItem("token")
            }
        })
        .then(response => {
        return response.data; 
        })
        .then(data => {
            setBucketName(data.bucket_name)
            setBucketPeriod(data.bucket_period)
            setBucketInvestment(data.investment_amount)

            const stockSymboltoStockNameMap = {};
            for (const item of allStocksList) {
                const [name, symbol] = item.split('=>');
                stockSymboltoStockNameMap[symbol] = name;
            }

            const selectedStocks = data.bucket_stocks.map(stock => `${stockSymboltoStockNameMap[stock.stock_code]}=>${stock.stock_code}`);
            setSelectedStocks(selectedStocks)
        })
        .catch(error => {
        // Handle any errors that occur during the request.
            console.error("Error fetching data:", error);
        });
    }, [allStocksList]);


    const handleBucketNameUpdateChange = (event) => {
        setBucketName(event.target.value);
    };

    const handleBucketPeriodSliderUpdateChange = (event, newValue) => {
        setBucketPeriod(newValue);
    };

    const handleBucketInvestmentUpdateChange = (event) => {
        setBucketInvestment(event.target.value);
    };

    const handleStocksListUpdateChange= (event) => {
        setSelectedStocks(event.target.value);
    };

    const renderChipValue=(selected) => {
        return (
            <div style={{fontWeight:"bold"}}>

            {selected.map((value) => (
                <Chip key={value} label={value} />
            ))
            }
            </div>
        )
    }

    const handleSubmit = (event) => {
        event.preventDefault();
        setLoading(true);

        const symbolList = selectedStocks.map(item => {
            const [name, symbol] = item.split('=>');
            return symbol;
        });

        console.log(JSON.stringify({
            "bucket_name": bucketName,
            "bucket_stocks": symbolList,
            "bucket_period": parseInt(bucketPeriod),
            "investment_amount":parseFloat(bucketInvestment),
        }));

        const bucketUpdateUrl = `http://localhost:3000/bucket/update?id=${id}&stock_index=${stockIndex}` 
        axios.put(bucketUpdateUrl, {
            "bucket_name": bucketName,
            "bucket_stocks": symbolList,
            "bucket_period": parseInt(bucketPeriod),
            "investment_amount":parseFloat(bucketInvestment),
        }, {
            headers: {
                "Content-type": "application/json",
                "Authorization": "Bearer " + localStorage.getItem("token")
            }
        })
        .then(response => {
            setLoading(false);
            return response.data;
        })
        .then(data => {
            window.alert(`bucket ${data.bucket_name} updated successfully.`);
            navigate(`/bucket/all?stockIndex=${stockIndex}`)
        })
        .catch(error => {
            setLoading(false);
            if (error.response && error.response.status === 401) {
                console.error("Unauthorized: ", error);
                navigate("/home")
            } else {
                console.error("Error during updating bucket request---->", error.response.data.error);
                window.alert(`Error during updating bucket request ${error.response.data.error}`)
            }
        });
    };

    return (
    <div className="center-container">
        {loading ? (
            <div className="center-content">
                <CircularProgress /> {/* Displays the centered loading indicator */}
            </div>
        ) : (
        <Container>
            <form onSubmit={handleSubmit}>
                <Grid container spacing={2}>
                <Grid item xs={12}>
                    <TextField
                    label="Bucket Name"
                    fullWidth
                    value={bucketName}
                    onChange={handleBucketNameUpdateChange}
                    />
                </Grid>

                <Grid item xs={12}>
                        <Box>
                        <Typography variant="subtitle1">
                            Bucket Period (Years)
                        </Typography>
                        <Slider defaultValue={10} value={bucketPeriod} min={1} max={25} onChange={handleBucketPeriodSliderUpdateChange} aria-label="Default" valueLabelDisplay="auto" ></Slider>
                        </Box>
                </Grid>

                <Grid item xs={12}>
                    <TextField
                    label="Bucket Investment (USD)"
                    fullWidth
                    value={bucketInvestment}
                    onChange={handleBucketInvestmentUpdateChange}
                    />
                </Grid>

                <Grid item xs={12}>
                    <FormControl fullWidth>
                    <InputLabel>Select Stocks For Bucket</InputLabel>
                    <Select
                        labelId="simple-select-label"
                        multiple
                        value={selectedStocks}
                        onChange={handleStocksListUpdateChange}
                        renderValue={renderChipValue}
                        MenuProps={{
                            anchorOrigin: {
                                vertical: "bottom",
                                horizontal: "left",
                            },
                            transformOrigin: {
                                vertical: "top",
                                horizontal: "left",
                            },
                            PaperProps: {
                                style: {
                                    maxHeight: 200,
                                    width: 250,
                                },
                            },
                        }}
                    >
                            {allStocksList.map((value) => {
                                return (<MenuItem key={value} value={value}>
                                     {value}
                                    {/* {value[0]} {value[1]} */}
                                </MenuItem>)
                            })}
                    </Select>

                    </FormControl>
                </Grid>

                <Grid item xs={12}>
                    <Button type="submit" variant="contained" stocks="primary">
                    Submit
                    </Button>
                </Grid>

                </Grid>
            </form>
        </Container>
        )}
    </div>
    );
    
};

export default UpdateBucket;

