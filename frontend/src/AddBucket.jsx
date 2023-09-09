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
import {useLocation, useNavigate} from "react-router-dom";
import CircularProgress from '@mui/material/CircularProgress';
import Slider from '@mui/material/Slider';
import Box from '@mui/material/Box';
import { Typography } from '@mui/material';
import './App.css'

const AddBucket = () => {
    const navigate = useNavigate()
    
    const [bucketName, setBucketName] = useState('');
    const [bucketPeriod, setBucketPeriod] = useState(10);
    const [bucketInvestment, setBucketInvestment] = useState('');
    const [allStocksList, setAllStocksList] = useState([])
    const [selectedStocks, setSelectedStocks] = useState([]);

    // loading symbol
    const [loading, setLoading] = useState(false);

    const location = useLocation();
    const searchParams = new URLSearchParams(location.search);
    const stockIndex = searchParams.get('stockIndex');

    useEffect(() => {
        axios.get(`http://localhost:3000/stock/list?stock_index=${stockIndex}`, {
            headers: {
            Authorization: "Bearer " + localStorage.getItem("token")
            }
        })
        .then(response => {
        return response.data; // Axios already parses the response JSON, so you can directly access the data property.
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

    const handleBucketNameChange = (event) => {
        setBucketName(event.target.value);
    };

    const handleBucketPeriodSliderChange = (event, newValue) => {
        setBucketPeriod(newValue);
    };
    
    const handleBucketInvestmentChange = (event) => {
        setBucketInvestment(event.target.value);
    };
    
    const handleStocksListChange= (event) => {
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

        axios.post(`http://localhost:3000/bucket/add?stock_index=${stockIndex}`, {
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
            console.log(data);
            window.alert(`New bucket ${data.bucket_name} added successfully.`);
            navigate(`/bucket/all?stockIndex=${stockIndex}`)
        })
        .catch(error=>{
            setLoading(false);
            if (error.response && error.response.status === 401) {
                console.error("Unauthorized: ", error);
                navigate("/home")
            } else {
                console.error("Error during adding bucket request---->", error.response.data.error);
                window.alert(`Error during adding bucket request ${error.response.data.error}`)
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
                        label={
                            <Typography variant="subtitle1">
                                Bucket Name
                            </Typography>
                        }
                        fullWidth
                        type='text'
                        value={bucketName}
                        onChange={handleBucketNameChange}
                        />
                    </Grid>

                    <Grid item xs={12}>
                        <Box>
                        <Typography variant="subtitle1">
                            Bucket Period (Years)
                        </Typography>
                        <Slider defaultValue={10} min={1} max={25} onChange={handleBucketPeriodSliderChange} aria-label="Default" valueLabelDisplay="auto" ></Slider>
                        </Box>
                    </Grid>

                    <Grid item xs={12}>
                        {stockIndex=="nasdaq" ? (
                            <TextField
                            label="Bucket Investment (USD)"
                            fullWidth
                            type='number'
                            value={bucketInvestment}
                            onChange={handleBucketInvestmentChange}
                            />
                        ):(
                            <TextField
                            label="Bucket Investment (INR)"
                            fullWidth
                            type='number'
                            value={bucketInvestment}
                            onChange={handleBucketInvestmentChange}
                            />
                        )}
                    </Grid>

                    <Grid item xs={12}>
                        <FormControl fullWidth>
                        <InputLabel>Select Stocks For Bucket</InputLabel>
                        <Select
                            labelId="simple-select-label"
                            multiple
                            value={selectedStocks}
                            onChange={handleStocksListChange}
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
                                </MenuItem>)
                            })}
                        </Select>
                        </FormControl>
                    </Grid>

                    <Grid item xs={12}>
                        <Button type="submit" variant="contained">
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

export default AddBucket;

