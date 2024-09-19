import { useLocation } from 'react-router-dom';

import { useTranslation } from "react-i18next";

import Scale from '@mui/icons-material/Scale';
import Event from '@mui/icons-material/Event';
import Folder from '@mui/icons-material/Folder';
import Calculate from '@mui/icons-material/Calculate';
import AssignmentInd from '@mui/icons-material/AssignmentInd';
import FitnessCenter from '@mui/icons-material/FitnessCenter';
import HomeRoundedIcon from '@mui/icons-material/HomeRounded';

import List from '@mui/material/List';
import Stack from '@mui/material/Stack';
import Divider from '@mui/material/Divider';
import ListItem from '@mui/material/ListItem';
import Typography from '@mui/material/Typography';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import ListItemButton from '@mui/material/ListItemButton';

import { useAuth } from '../AuthProvider';

import LanguageSelect from './LanguageSelect';
import LoginLogoutButton from './LoginLogoutButton';
import { ColorSchemeTabsBasic } from './ColorModeSwitch';


export default function MenuContent() {
  let location = useLocation();
  const { t } = useTranslation();
  const { isAuth } = useAuth();


  const mainListItems = [
    { text: t("menu_content.home"), icon: <HomeRoundedIcon />, href: '/home', authRequired: false },
    { text: t('menu_content.exercises'), icon: <FitnessCenter />, href: '/exercise', authRequired: false },
    { text: t('menu_content.calculator'), icon: <Calculate />, href: '/calculator', authRequired: false },
    { text: t('menu_content.profile'), icon: <AssignmentInd />, href: '/profile', authRequired: true },
    { text: t('menu_content.templates'), icon: <Folder />, href: '/template', authRequired: true },
    { text: t('menu_content.workouts'), icon: <Event />, href: '/workout', authRequired: true },
    { text: t('menu_content.weight'), icon: <Scale />, href: '/weight', authRequired: true },
  ];

  return (
    <>
      <Stack sx={{ flexGrow: 1 }}>
        <Stack sx={{ flexGrow: 1, px: 1, pt: 1, justifyContent: 'space-between' }}>
          <List dense>
            {mainListItems.map((item, index) => {
              if (isAuth || !item.authRequired)
                return (
                  <ListItem key={index} disablePadding sx={{ display: 'block' }}>
                    <ListItemButton selected={item.href === location.pathname} href={item.href}>
                      <ListItemIcon>{item.icon}</ListItemIcon>
                      <ListItemText primary={<Typography variant="body1">{item.text}</Typography>} />
                    </ListItemButton>
                  </ListItem>
                )
            })}
          </List>
          <Stack>
            <Divider />
            <Stack sx={{ alignItems: 'center', p: 1 }} spacing={1}>
              <LanguageSelect />
              <ColorSchemeTabsBasic />
            </Stack>
          </Stack>
        </Stack>
        <Divider />
        <Stack sx={{ p: 2 }}>
          <LoginLogoutButton />
        </Stack>
      </Stack>
    </>
  );
}
