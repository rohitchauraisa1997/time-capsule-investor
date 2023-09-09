import {useEffect, useState} from "react";
import axios from 'axios';
import { Card, Typography, Button,IconButton } from "@mui/material";
import { useNavigate } from "react-router-dom";
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete';
import {useLocation} from "react-router-dom";

import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';

function BucketCards(){
    const [buckets, setBuckets] = useState([])
    const navigate = useNavigate()

    const location = useLocation();
    const searchParams = new URLSearchParams(location.search);
    const stockIndexFromURL = searchParams.get('stockIndex');

    const [stockIndex, setStockIndex] = useState(stockIndexFromURL||'nasdaq');

    const handleChange = (event) => {
        setStockIndex(event.target.value);
    };

    useEffect(()=>{
        axios.get(`http://localhost:3000/bucket/all?stock_index=${stockIndex}`, {
            headers: {
            Authorization: "Bearer " + localStorage.getItem("token")
            }
        })
        .then(response => {
            return response.data;
        })
        .then(data => {
            setBuckets(data);
        })
        .catch((error) => {
            if (error.response && error.response.status === 401) {
                console.error("Unauthorized: ", error);
                navigate("/home")
            } else {
                console.error("Error during all bucketCards request", error);
            }
        }
        );
    },[stockIndex])

    const handleAddNewBucketClick = ()=>{
        navigate(`/bucket/add?stockIndex=${stockIndex}`)
    }

    return (
    <div style={{marginTop:"1vh"}}>
        <div style={{  position: "relative", width:"100vw",height:"1vh", 
            // backgroundColor:"red"
        }}>

            <FormControl sx={{ m: 1, minWidth: 80, width:170 }}>
                <InputLabel id="demo-simple-select-autowidth-label" width="170">Select Stock Index</InputLabel>
                <Select
                    labelId="demo-simple-select-autowidth-label"
                    id="demo-simple-select-autowidth"
                    value={stockIndex}
                    onChange={handleChange}
                    autoWidth
                    label="Age"
                >
                <MenuItem value={"nasdaq"}>
                    {/* <Typography variant="h6" component="div" fontWeight="bold"> */}
                        S&P 500
                    {/* </Typography> */}
                </MenuItem>
                <MenuItem value={"nse"}>
                    {/* <Typography variant="h6" component="div" fontWeight="bold"> */}
                        Nifty50
                    {/* </Typography> */}
                </MenuItem>
                </Select>
            </FormControl>

            <Button 
                variant="contained" 
                color="secondary" 
                style={{position:"absolute",top: 0, right:30}}
                onClick={handleAddNewBucketClick}
            >
                Add New Bucket
            </Button>
        </div>

        <div style={{
            display: "flex", 
            flexWrap: "wrap", 
            justifyContent: "center", 
            marginTop: 60, 
            position: "relative"
        }}>
            {buckets.length === 0 ? (
                <div style={{textAlign:"center"}}>
                    <Typography variant="h5" component="div" fontWeight="bold">
                        WOW SO EMPTY! <br />
                        Add A New Bucket To Track Your Gains..
                    </Typography>
                </div>
            ) : (
                buckets.map((bucket, index) => (
                    <BucketCard 
                        key={index} 
                        bucket={bucket} 
                        index={index} 
                        buckets={buckets} 
                        setBuckets={setBuckets} 
                        stockIndex={stockIndex}
                    />
                ))
            )}
        </div>

    </div>
    )
}

function BucketCard(props) {

    const navigate = useNavigate()
    const initialBuckets = props.buckets
    const indexToDelete = props.index
    const setBuckets = props.setBuckets
    const stockIndex = props.stockIndex

    const handleFindGainsClick =(id)=>{
        const queryId = {
            'id': id,
            'stockIndex':stockIndex
        }
        const queryString = new URLSearchParams(queryId).toString();
        const url = `/bucket/profit?${queryString}`
        navigate(url)
    }

    const handleDeleteClick =(id)=>{
        const queryId = {
            'id': id,
            'stock_index':stockIndex
        }
        const queryString = new URLSearchParams(queryId).toString();
        const url = `http://localhost:3000/bucket/delete?${queryString}`
        axios.delete(url, {
            headers:{
                Authorization: "Bearer " +localStorage.getItem("token")
            }
        })
        .then(response => {
            return response.data;
        })
        .then(data=>{
            const newBuckets = initialBuckets.filter((bucket, index) => index !== indexToDelete);
            setBuckets(newBuckets);
            return data
        })  
        .catch((error) => {
            if (error.response && error.response.status === 401) {
                console.error("Unauthorized: ", error);
                navigate("/home")
            } else {
                console.error("Error during single bucketcard request", error);
            }
        }
        )
    }

    const handleUpdateClick =(id)=>{
        const queryId = {
            'id': id,
            'stockIndex':stockIndex
        }
        const queryString = new URLSearchParams(queryId).toString();
        const url = `/bucket/update?${queryString}`
        navigate(url)
    }

    return (

        <Card style={{  
            margin: 10,
            width: 350,
            minHeight: 200,
            display: 'flex',
            flexDirection: 'column', // Align items vertically
            justifyContent: 'space-between', // Distribute items along the available space
            padding: '10px',
            boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)',
            borderRadius: '8px',
        }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '10px' }}>
                {/* Update Button */}
                <Typography color="secondary" variant="h6" onClick={() => handleFindGainsClick(props.bucket._id)} style={{cursor : 'pointer'}} >
                    <span style={{textTransform:"capitalize"}}>{props.bucket.bucket_name}</span>
                    {stockIndex=="nasdaq" ? (
                        <div style={{fontSize:"14px"}}> Investment ${props.bucket.investment_amount}</div>
                    ):(
                        <div style={{fontSize:"14px"}}> Investment ₹{props.bucket.investment_amount}</div>
                    )}
                    <div style={{fontSize:"14px"}}> Period {props.bucket.bucket_period} Year(s)</div>
                </Typography>
                    <div>
                        <IconButton onClick={() => handleUpdateClick(props.bucket._id)}>
                            <EditIcon />
                        </IconButton>
                        <IconButton onClick={() => handleDeleteClick(props.bucket._id)}>
                            <DeleteIcon />
                        </IconButton>
                    </div>
            </div>
            {/* <Typography textAlign="center" variant="h6">{props.bucket.bucket_period} Years</Typography> */}
            {/* <div style={{ marginTop: '10px', justifyContent:"left", textAlign:"left"}}> */}
            <div style={{ 
                marginTop: '10px',
                textAlign:"left",
                justifyContent:"left",
                marginBottom: '10px',
            }}>
                {props.bucket.bucket_stocks.map(stock => (
                    <BucketStockName key={stock.stock_code} stock={stock} stock_index={stockIndex} />
                ))}
            </div>
            <Button variant="contained" color="secondary" cursor='pointer' onClick={() => handleFindGainsClick(props.bucket._id)}>
                Find Gains!
            </Button>
        </Card>
    );
}

function BucketStockName(props) {
    const navigate = useNavigate()
    
    const handleRenderGraphClick =(stock_code, stock_index)=>{
        const queryId = {
            'stockCode': stock_code,
            'stockIndex': stock_index
        }
        const queryString = new URLSearchParams(queryId).toString();
        const url = `/stock/render?${queryString}`
        window.open(url)
    }

    return (
        // <Typography textAlign={"center"} variant="subtitle1" color="primary" fontWeight="bold" onClick={() => handleRenderGraphClick(props.stock.stock_code, props.stock_index)} style={{cursor : 'pointer'}} >
        <Typography variant="subtitle1" color="primary" fontWeight="bold" onClick={() => handleRenderGraphClick(props.stock.stock_code, props.stock_index)} style={{cursor : 'pointer'}} >
            {props.stock.stock_code} 
            <span style={{fontSize:"12px", marginLeft:"2px"}}> [{props.stock.stock_name}] </span>
        </Typography>
    );
}

export default BucketCards