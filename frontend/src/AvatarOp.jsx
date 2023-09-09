import { useState } from 'react';
import Avatar from '@mui/material/Avatar';
import Menu from '@mui/material/Menu';
import MenuItem from '@mui/material/MenuItem';
import Typography from '@mui/material/Typography';
import { purple } from '@mui/material/colors';
import Logout from '@mui/icons-material/Logout';
import ListItemIcon from '@mui/material/ListItemIcon';

const AvatarWithLogoutOptions = (props) => {
    const [anchorEl, setAnchorEl] = useState(null);

    const handleAvatarClick = (event) => {
        setAnchorEl(event.currentTarget);
    };

    const handleClose = () => {
        setAnchorEl(null);
    };

    const handleUserLogoutClick = () => {
        localStorage.setItem("token", null)
        // setUserEmail(null)
        // TODO: Find a better way than window.location to render Appbar without reload and handle the "authenticated" state variable correctly in App.jsx .
        // navigate("/home")   
        window.location = "/home";
    };

    return (
        <div>

            <Avatar
                alt="User Avatar"
                onClick={handleAvatarClick}
                style={{cursor:"pointer", marginRight:"20px"}}
                sx={{bgcolor:purple[500]}}
            >
                <Typography variant="body1" style={{ fontWeight: 'bold', fontFamily: 'Arial' }}>
                    {props.userName[0].toUpperCase()}
                </Typography>
            </Avatar>
            <Menu
                anchorEl={anchorEl}
                open={Boolean(anchorEl)}
                onClose={handleClose}
            >
                <MenuItem key="logout" onClick={handleUserLogoutClick}>
                    <ListItemIcon>
                        <Logout fontSize="small" />
                    </ListItemIcon>
                    Logout
                </MenuItem>
            </Menu>

        </div>
    );
};

export default AvatarWithLogoutOptions;
