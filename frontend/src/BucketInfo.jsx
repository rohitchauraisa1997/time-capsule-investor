import { useState, useEffect } from 'react';
import {useLocation, useNavigate } from 'react-router-dom';
import axios from 'axios';
import { Paper, Button, Typography } from "@mui/material";

import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogContentText from '@mui/material/DialogContentText';
import DialogTitle from '@mui/material/DialogTitle';

import CircularProgress from '@mui/material/CircularProgress';

import Alert from '@mui/material/Alert';
import './TransitionScreen.css';
import { purple } from '@mui/material/colors';

function formatNumericals(earnings) {
    const formatter = new Intl.NumberFormat('en-US', {
        minimumFractionDigits: 0,
        maximumFractionDigits: 2,
    });
    return formatter.format(earnings);
}

function formatEarningsUsd(earnings) {
    const formatter = new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
        minimumFractionDigits: 0,
        maximumFractionDigits: 4,
    });
    return formatter.format(earnings);
}

function formatEarningsInr(earnings) {
    const formatter = new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'INR',
        minimumFractionDigits: 0,
        maximumFractionDigits: 2,
    });
    return formatter.format(earnings);
}

function BucketInfo() {
    const location = useLocation();
    const searchParams = new URLSearchParams(location.search);
    const id = searchParams.get('id');
    const stockIndex = searchParams.get('stockIndex');

    const bucketProfitUrl = `http://localhost:3000/bucket/profit?id=${id}&stock_index=${stockIndex}`

    const [bucketInfo, setBucketInfo] = useState("");
    const navigate = useNavigate()

    useEffect(() => {
        axios.get(bucketProfitUrl,{
            headers:{
                Authorization: "Bearer " + localStorage.getItem("token")
            }
        })
        .then(response=>{
            return response.data;
        })
        .then(data=>{
            setBucketInfo(data)
        })
        .catch(error=>{
            if (error.response && error.response.status === 401) {
                console.error("Unauthorized: ", error);
                navigate("/home")
            } else {
                console.error("Error during bucketInfo request", error);
            }
        })
    },[])

    if (!bucketInfo) {
        return <div>Loading...</div>; // or handle the loading state in some other way
    }

    return (
        <div>
        {
            <div className="transition-screen">
                <span className="transition-content">
                    {bucketInfo.percentage_gains >= 0 ?(
                        <Typography variant='h2' style={{color:"rgba(0, 255, 0, 0.8)"}}>
                            Bucket Profit {bucketInfo.percentage_gains.toFixed(2)}%
                        </Typography>
                    ):(
                        <Typography variant='h2' style={{color:"rgba(255, 0, 0, 0.8)"}}>
                            Bucket Loss {bucketInfo.percentage_gains}%
                        </Typography>
                    )}
                </span>
            </div>
        }
        {/* <div style={{ marginTop: 30 }}> */}
        <Paper elevation={3} style={{ padding: '20px', marginBottom: '20px' }}>
            <div style={{ textAlign: 'center', margin: '0 auto' }}>
                <Typography variant="h4" color="secondary" textTransform="uppercase">
                    <span style={{textTransform:"capitalize"}}>{bucketInfo.bucket_name} </span>
                </Typography>
                <div style={{fontSize:"16px", color:"purple", fontWeight:"bold"}}> Period {bucketInfo.bucket_period} Year(s)</div>
                {stockIndex=="nasdaq" ? (
                    <Typography variant="h6" color="secondary">
                        Investment Amount: <strong> {formatEarningsUsd(bucketInfo.investment_amount)} </strong>
                    </Typography>):(
                    <Typography variant="h6" color="secondary">
                        Investment Amount: <strong> {formatEarningsInr(bucketInfo.investment_amount)} </strong>
                    </Typography>
                    )
                }
            </div>
        </Paper>

        <div style={{display: "flex", flexWrap: "wrap", justifyContent:'space-evenly'}}>
            {bucketInfo.bucket_stocks.map((stock, index) => (
                    <BucketStockInfo key={index} index={index} stock={stock} stock_index={stockIndex}/>
            ))}
        </div>

        <Paper elevation={3} 
            style={{ 
                display: 'flex',
                justifyContent: 'center',
                alignItems: 'center',
                height: '250px',
            }}
        >
            <div>
                <h2>---------Bucket's Overall Performance---------</h2>
                <div className='key-value-container'>
                    <div className="key" style={{fontSize:"20px"}}>
                        Initial Bucket Investment:
                    </div>
                    {stockIndex=="nasdaq" ? (
                        <div className='value' style={{fontSize:"20px", color: purple[600] }}>
                            {formatEarningsUsd(bucketInfo.investment_amount)}
                        </div>
                    ):(
                        <div className='value' style={{fontSize:"20px", color: bucketInfo.final_investment >= 0 ? '#00C853' : '#FF1744' }}>
                            {formatEarningsInr(bucketInfo.investment_amount)}
                        </div>
                    )}

                    <div className="key" style={{fontSize:"20px"}}>
                        Final Bucket Investment:
                    </div>
                    {stockIndex=="nasdaq" ? (
                        <div className='value' style={{fontSize:"20px", color: bucketInfo.final_investment >= 0 ? '#00C853' : '#FF1744' }}>
                            {formatEarningsUsd(bucketInfo.final_investment)}
                        </div>
                    ):(
                        <div className='value' style={{fontSize:"20px", color: bucketInfo.final_investment >= 0 ? '#00C853' : '#FF1744' }}>
                            {formatEarningsInr(bucketInfo.final_investment)}
                        </div>
                    )}

                    <div className="key" style={{fontSize:"20px"}}>
                        Profit/Loss: 
                    </div>
                    {stockIndex=="nasdaq" ? (
                        <div className="value" style={{fontSize:"20px", color: bucketInfo.monetary_gains >= 0 ? '#00C853' : '#FF1744' }}>
                            {formatEarningsUsd(bucketInfo.monetary_gains)}
                        </div>
                    ):(
                        <div className="value" style={{fontSize:"20px", color: bucketInfo.monetary_gains >= 0 ? '#00C853' : '#FF1744' }}>
                            {formatEarningsInr(bucketInfo.monetary_gains)}
                        </div>
                    )}

                    <div className="key" style={{fontSize:"20px"}}>
                        Profit/Loss Percentage:  
                    </div>
                    <div className="value" style={{fontSize:"20px", color: bucketInfo.percentage_gains >= 0 ? '#00C853' : '#FF1744' }}>
                        {formatNumericals(bucketInfo.percentage_gains)}%
                    </div>

                </div>
            </div>
        </Paper>

    </div>
    );
}

const formatDate = (dateString) => {
    const options = { year: 'numeric', month: 'long', day: 'numeric' };
    return new Date(dateString).toLocaleDateString(undefined, options);
};

function BucketStockInfo(props){
    const navigate = useNavigate()

    const handleRenderGraphClick =(stockCode, stockIndex)=>{
        const queryId = {
            'stockCode': stockCode,
            'stockIndex':stockIndex
        }
        const queryString = new URLSearchParams(queryId).toString();
        const url = `/stock/render?${queryString}`
        // navigate(url)
        window.open(url)
    }

    const [open, setOpen] = useState(false);

    const [stockPrice, setStockPrice] = useState()

    const [loading, setLoading] = useState(false);
    const handleDialogOpen = (stockCode) => {
        setLoading(true);
        axios.get(`http://localhost:3000/kite/ltp?symbol=${stockCode}`)
        .then(response=>{
            return response.data
        })
        .then(data=>{
            setStockPrice(data)
        })
        .catch((error) => {
            if (error.response && error.response.status === 401) {
                console.error("Unauthorized: ", error);
                navigate("/home")
            } else {
                console.error("Error during ltp request to kite", error);
            }
        }
        )
        .finally(() => {
            setLoading(false); // Request completed, stop loading
            setOpen(true);
        });
        setOpen(true);
    };

    const handleDialogClose = () => {
        setOpen(false);
    };

    const [alert, setAlert] = useState(0)
    const [transactionId, setTransactionId] = useState("")

    const handleBuyOneStockConfirmDialogClick = (stockCode) => {
        setLoading(true);
        axios.get(`http://localhost:3000/kite/gtt/buy?symbol=${stockCode}`)
        .then(response=>{
            return response.data
        })
        .then(data=>{
            setLoading(false); // Request completed, stop loading
            setOpen(false);
            setTransactionId(data)
            setAlert(1)
            // Set the alert to false after 15 seconds
            // to hide the alert notification after some time..
            // setTimeout(() => {
            //     setAlert(false);
            // }, 15000);
        })
        .catch((error) => {
            setLoading(false); // Request completed, stop loading
            setOpen(false);
            setAlert(2)
            if (error.response && error.response.status === 401) {
                console.error("Unauthorized: ", error);
                navigate("/home")
            } else {
                console.error("Error during gtt buy to kite", error);
            }
            return
        }
        )
    };

    return (
        <Paper elevation={3} style={{ padding: '20px', marginBottom: '20px', display: 'flex', flexDirection: 'column' }}>
            {
                alert === 1 ? (
                    <Alert severity="success">
                        GTT order placed. Transaction Id {transactionId}. Verify in kite console.
                    </Alert>
                ) : alert === 2 ? (
                    <Alert severity="error">
                        Error During GTT Order.
                    </Alert>
                ) : null
            }
            <Typography variant="h6" color="secondary">
                Stock #{props.index + 1} {props.stock.stock_code} <span style={{fontSize:"13px"}}> [{props.stock.stock_name}]</span>
            </Typography>
                    <div className='key-value-container'>
                        <div className='key'>
                            Gain/Loss Percentage:
                        </div>
                        <div className='value' style={{ color: props.stock.percentage_gains >= 0 ? '#00C853' : '#FF1744' }}>
                            {formatNumericals(props.stock.percentage_gains)}%
                        </div>
                
                    <div className='key'>
                        Gain/Loss: 
                    </div>
                    <div className='value' style={{ color: props.stock.monetary_gains >= 0 ? '#00C853' : '#FF1744' }}>
                        {props.stock_index=="nasdaq" ?(
                            <span>
                                {formatEarningsUsd(props.stock.monetary_gains)}
                            </span>
                        ):(
                            <span>
                                {formatEarningsInr(props.stock.monetary_gains)}
                            </span>
                        )
                        }
                    </div>

                    <div className='key'>
                        Final Investment:
                    </div>
                    <div className='value' style={{color:purple[600]}}>
                        {props.stock_index=="nasdaq" ?(
                            <span>
                                {formatEarningsUsd(props.stock.final_investment_in_stock)}
                            </span>
                        ):(
                            <span>
                                {formatEarningsInr(props.stock.final_investment_in_stock)}
                            </span>
                        )
                        }
                    </div>

                    <div className='key'>
                        Initial Investment:
                    </div>
                    <div className='value' style={{color:purple[600]}}>
                        {props.stock_index=="nasdaq" ?(
                            <span >
                                {formatEarningsUsd(props.stock.initial_investment_in_stock)}
                            </span>
                        ):(
                            <span >
                                {formatEarningsInr(props.stock.initial_investment_in_stock)}
                            </span>
                        )
                        }
                    </div>

                    <div className='key'>
                        Final Stock Price:
                    </div>
                    <div className='value' style={{color:purple[600]}}>
                        {props.stock_index=="nasdaq" ?(
                            <span>
                                {formatEarningsUsd(props.stock.final_price)}
                            </span>
                        ):(
                            <span>
                                {formatEarningsInr(props.stock.final_price)}
                            </span>
                        )
                        }
                    </div>

                    <div className='key'>
                        Initial Stock Price:
                    </div>
                    <div className='value' style={{color:purple[600]}}>
                        {props.stock_index=="nasdaq" ?(
                            <span>
                                {formatEarningsUsd(props.stock.initial_stock_allocated_price)}
                            </span>
                        ):(
                            <span>
                                {formatEarningsInr(props.stock.initial_stock_allocated_price)}
                            </span>
                        )
                        }
                    </div>

                    <div className='key'>
                        Stock Count: 
                    </div>
                    <div className='value' style={{color:purple[600]}}>
                        {formatNumericals(props.stock.initial_stock_allocated_count)}
                    </div>

                    <div className='key'>
                        Stock Buying Date:
                    </div>
                    <div className='value'>
                        {formatDate(props.stock.stock_buying_date)}
                    </div>

                    <div className='key'>
                        Final Date:
                    </div>
                    <div className='value'>
                        {formatDate(props.stock.final_date)}
                    </div>
                    </div>

                <br/>
            <div style={{ marginTop: 'auto', textAlign: 'center', marginBottom: 'auto' }}>

                <Button variant="contained" color="secondary" onClick={() => handleRenderGraphClick(props.stock.stock_code, props.stock_index)}>
                    Render Graph!
                </Button>

                {props.stock_index == 'nse' && (
                <div style={{marginTop:10}}>

                    <Button  variant="contained" color="secondary" onClick={() => handleDialogOpen(props.stock.stock_code)}>
                        Buy One Stock!
                    </Button>

                    <Dialog
                    open={open}
                    onClose={handleDialogClose}
                    aria-labelledby="alert-dialog-title"
                    aria-describedby="alert-dialog-description"
                    >
                        <DialogTitle id="alert-dialog-title">
                            {"GTT Order Buy Alert!"}
                        </DialogTitle>
                        <DialogContent style={{width:500}}>
                        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', minHeight: '100px' }}>
                            {loading ? (
                                <CircularProgress />
                            ) : (
                                <DialogContentText id="alert-dialog-description" style={{justifyContent:"center", textAlign:"center"}}>
                                    LTP for <strong> {props.stock.stock_code}</strong> = <strong>{stockPrice}</strong> <br />
                                    Are You Sure You Want to Buy 1 stock of <strong> {props.stock.stock_code}</strong> for <strong> {0.9*stockPrice} </strong>?
                                </DialogContentText>
                            )}
                        </div>
                        </DialogContent>
                        <DialogActions>
                            <Button onClick={handleDialogClose}>Reject</Button>
                            <Button onClick={() => handleBuyOneStockConfirmDialogClick(props.stock.stock_code)} autoFocus>
                            Confirm
                            </Button>
                        </DialogActions>
                    </Dialog>
                </div>
                )}
            </div>
        </Paper>
    );
}

export default BucketInfo;