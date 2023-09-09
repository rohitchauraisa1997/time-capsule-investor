import AppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import Button from '@mui/material/Button';
// import Typography from '@mui/material/Typography';
import axios from 'axios';
import { useState, useEffect } from 'react';
import {useNavigate} from "react-router-dom";
import { Link, Typography } from '@mui/material';
import CircularProgress from '@mui/material/CircularProgress';
import AvatarWithLogoutOptions from './AvatarOp';
import { ThemeProvider } from '@mui/system'; // Import from @mui/system
import { createTheme } from '@mui/material/styles';

const darkTheme = createTheme({
    palette: {
      mode: 'dark',
      primary: {
        main: '#1976d2',
        },
    },
});


function BucketGainsAppBar (){
    const [userName, setUserEmail] = useState(null);
    const [loading, setLoading] = useState(true);
    const navigate = useNavigate()

    useEffect(()=>{
        axios.get("http://localhost:3000/user/me",{
            headers:{
                Authorization: "Bearer " + localStorage.getItem("token")
            }
        })
        .then(response => {
            // setLoading(false);
            return response.data.username;
        })
        .then(data=>{
            setUserEmail(data)
            setLoading(false); 
        })
        .catch(error=>{
            setLoading(false); 
            if (error.response && error.response.status === 401) {
                console.error("Unauthorized: ", error);
                // navigate("/home")
            } else {
                console.error("Error during /user/me validation route", error);
            }
        })
    },[])


    const handleUserSignInClick = ()=>{
        navigate("/signin")
    }

    const handleUserSignUpClick = ()=>{
        navigate("/signup")
    }

    if (loading) { // Show loading indicator while loading
        return (
            <div className="center-container">
                <div className="center-content">
                    <CircularProgress />
                    </div>
            </div>
        );
    } else if (userName ===null){
        return (
        <ThemeProvider theme={darkTheme}> 
            <AppBar position="static">
                <Toolbar>
                    <Typography sx={{ flexGrow: 1 }} variant='h5' fontWeight="bold">   
                        <Link color="textPrimary" underline='none' href="/bucket/all"> Time Capsule Investor</Link> 
                    </Typography>

                    <Button color="inherit" onClick={handleUserSignInClick}>SignIn</Button>
                    <Button color="inherit" onClick={handleUserSignUpClick}>SignUp</Button>
                </Toolbar>
            </AppBar>
        </ThemeProvider>
        )
    }else{
        return (
        <ThemeProvider theme={darkTheme}> 
            <AppBar position="static">
                <Toolbar>
                    <Typography sx={{ flexGrow: 1 }} variant='h5' fontWeight="bold">   
                        <Link color="textPrimary" underline='none' href="/bucket/all"> Time Capsule Investor</Link> 
                    </Typography>
                    
                    <AvatarWithLogoutOptions userName={userName}>
                    </AvatarWithLogoutOptions>

                </Toolbar>
            </AppBar>
        </ThemeProvider>
        )
    }
}

  

export default BucketGainsAppBar