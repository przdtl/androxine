import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import Stack from '@mui/material/Stack';
import HomeRoundedIcon from '@mui/icons-material/HomeRounded';
import SettingsRoundedIcon from '@mui/icons-material/SettingsRounded';
import Button from '@mui/material/Button';
import Divider from '@mui/material/Divider';
import Scale from '@mui/icons-material/Scale';
import LogoutRoundedIcon from '@mui/icons-material/LogoutRounded';
import LoginRoundedIcon from '@mui/icons-material/LoginRounded';
import Calculate from '@mui/icons-material/Calculate';
import Folder from '@mui/icons-material/Folder';
import AssignmentInd from '@mui/icons-material/AssignmentInd';
import FitnessCenter from '@mui/icons-material/FitnessCenter';
import Event from '@mui/icons-material/Event';
import { useAuth } from '../UserProvider';

const mainListItems = [
  { text: 'Home', icon: <HomeRoundedIcon />, href: '/' },
  { text: 'Exercises', icon: <FitnessCenter />, href: '/exercises' },
  { text: 'Calculator', icon: <Calculate />, href: '/calculator' },
  { text: 'Profile', icon: <AssignmentInd />, href: '/auth' },
  { text: 'Templates', icon: <Folder />, href: '/templates' },
  { text: 'Workouts', icon: <Event />, href: '/workouts' },
  { text: 'Weight', icon: <Scale />, href: '/weight' },
];

const secondaryListItems = [
  { text: 'Settings', icon: <SettingsRoundedIcon />, href: '/settings' },
];

export default function MenuContent() {
  const { isAuth, user, login, logout } = useAuth();

  return (
    <Stack sx={{ flexGrow: 1 }}>
      <Stack sx={{ flexGrow: 1, p: 1, justifyContent: 'space-between' }}>
        <List dense>
          {mainListItems.map((item, index) => (
            <ListItem key={index} disablePadding sx={{ display: 'block' }}>
              <ListItemButton selected={index === 0} href={item.href}>
                <ListItemIcon>{item.icon}</ListItemIcon>
                <ListItemText primary={item.text} />
              </ListItemButton>
            </ListItem>
          ))}
        </List>
        <List dense>
          {secondaryListItems.map((item, index) => (
            <ListItem key={index} disablePadding sx={{ display: 'block' }}>
              <ListItemButton href={item.href}>
                <ListItemIcon>{item.icon}</ListItemIcon>
                <ListItemText primary={item.text} />
              </ListItemButton>
            </ListItem>
          ))}
        </List>
      </Stack>
      <Divider />
      <Stack sx={{ p: 2 }}>
        <Button variant="outlined" fullWidth startIcon={isAuth ? <LogoutRoundedIcon /> : <LoginRoundedIcon />}>
          {isAuth ? 'Logout' : 'Login'}
        </Button>
      </Stack>
    </Stack>
  );
}
