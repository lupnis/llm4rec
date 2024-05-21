import { createApp } from 'vue';
import App from './App';
import router from './router';

import '@material/web/button/filled-button';
import '@material/web/button/text-button';
import '@material/web/button/filled-tonal-button';
import '@material/web/iconbutton/icon-button';
import '@material/web/iconbutton/filled-tonal-icon-button';
import '@material/web/textfield/outlined-text-field';
import '@material/web/textfield/filled-text-field';
import '@material/web/icon/icon';
import '@material/web/progress/circular-progress';
import '@material/web/progress/linear-progress';
import '@material/web/dialog/dialog';
import '@material/web/chips/assist-chip';
import '@material/web/chips/chip-set';
import '@material/web/chips/filter-chip';
import '@material/web/chips/input-chip';

import VueCookies from 'vue3-cookies';
import axios from 'axios';


const app = createApp(App);
app.use(router);
app.use(VueCookies);
app.provide('$http', axios);
app.mount('#app');
