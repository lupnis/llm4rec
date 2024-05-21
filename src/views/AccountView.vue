<template>
  <div class="about">
    <header>
      <md-text-button href="/">返回</md-text-button>
    </header>
    <div class="account-container" v-if="loggedIn">
      <h1>当前登录账户</h1>
      <hr />
      <h2>账户ID: {{ loggedInInfo.uid }}</h2>
      <h2>用户名: {{ loggedInInfo.uname }}</h2>
      <md-filled-button @click="logOut()" style="--md-filled-button-container-color: #880000;">注销</md-filled-button>
    </div>
    <div class="account-container" v-else-if="!loggingIn">
      <h1>选择登录账户</h1>
      <hr />
      <md-outlined-text-field label="账户ID" :value="accountid" @input="event => accountid = event?.target?.value">
      </md-outlined-text-field>
      <md-outlined-text-field label="密码" :value="pwd" type="password" @input="event => pwd = event?.target?.value">
      </md-outlined-text-field>
      <md-filled-button @click="loginBtnClicked()">登录</md-filled-button>
    </div>
    <md-dialog ref="loggingInDialog" type="alert" @closed="logginInDialogClosed">
      <div slot="headline">登录中...</div>
      <form slot="content">
        <div class="loading-container">
          <md-circular-progress four-color indeterminate></md-circular-progress>
          <a>正在验证登录...</a>
        </div>
      </form>
    </md-dialog>

    <md-dialog type="alert" ref="failedAuthDialog" @closed="this.failedAuth = false">
      <div slot="headline">
        {{ failedTitle }}
      </div>
      <form slot="content" id="form-authfailed" method="dialog">
        {{ failedDetails }}
      </form>
      <div slot="actions">
        <md-text-button form="form-authfailed">确认</md-text-button>
      </div>
    </md-dialog>


  </div>
</template>

<script>
import { Base64 } from 'js-base64';
import { md5 } from 'js-md5';
import axios from 'axios';
export default {
  name: 'AccountView',
  data() {
    return {
      loggedIn: false,
      loggedInInfo: {
        uid: '加载中...',
        uname: '加载中...'
      },
      accountid: '',
      pwd: '',
      loggingIn: false,
      failedAuth: false,
      failedTitle: '',
      failedDetails: ''
    }
  },
  watch: {
    loggingIn(nv) {
      if (nv == true) {
        this.$refs.loggingInDialog.show();
      } else {
        this.$refs.loggingInDialog.close();
      }
    },
    failedAuth(nv) {
      if (nv == true) {
        this.$refs.failedAuthDialog.show();
      } else {
        this.$refs.failedAuthDialog.close();
      }
    },
    loggedIn(nv) {
      if (nv == true) {
        this.verifyLogin();
        this.getLoginInfo();
      }
    }
  },
  mounted() {
    this.verifyLogin();
  },
  methods: {
    getNativeLoginInfo: function () {
      let uid = this.$cookies.get('uid');
      let sid = this.$cookies.get('sid');
      return [uid, sid];
    },
    doLogin: function (uid, pwd) {
      this.loggedIn = false;
      this.loggingIn = true;
      this.failedAuth = false;
      this.$cookies.remove('uid');
      this.$cookies.remove('sid');
      pwd = md5(Base64.encode(pwd));
      axios.post(`/api/user/login?username=${uid}&hashedpwd=${pwd}`)
        .then(resp => {
          this.loggingIn = false;
          let result = resp.data;
          if (result.status == 0) {
            this.failedTitle = '登录失败';
            this.failedDetails = '用户名或密码错误!';
            this.failedAuth = true;
          } else {
            this.$cookies.set('uid', uid);
            this.$cookies.set('sid', result.data);
            this.loggedIn = true;
          }
          this.accountid = this.pwd = '';
        }).catch(err => {
          this.failedTitle = '网络错误';
          this.failedDetails = '无法连接至API服务器!';
          this.failedAuth = true;
        });
    },
    verifyLogin: function () {
      let session_data = this.getNativeLoginInfo();
      let uid = session_data[0];
      let sid = session_data[1];
      if (uid == null || sid == null) {
        this.loggedIn = false;
      } else {
        axios.post(`/api/user/vlogin?uname=${uid}&sessionid=${sid}`)
          .then(resp => {
            this.loggingIn = false;
            let result = resp.data;
            if (result.status == 0) {
              this.loggedIn = false;
              this.failedTitle = '登录失效';
              this.failedDetails = '请重新登录!';
              this.failedAuth = true;
            } else {
              this.loggedIn = true;
            }
          }).catch(err => {
            this.failedTitle = '网络错误';
            this.failedDetails = '无法连接至API服务器!';
            this.failedAuth = true;
          })
      }
    },
    getLoginInfo: function () {
      let session_data = this.getNativeLoginInfo();
      let uid = session_data[0];
      let sid = session_data[1];
      if (uid == null || sid == null) {
        this.loggedIn = false;
        this.failedTitle = '登录过期';
        this.failedDetails = '请重新登录!';
        this.failedAuth = true;
      } else {
        axios.get(`/api/user/info?uname=${uid}&sessionid=${sid}`)
          .then(resp => {
            this.loggingIn = false;
            let result = resp.data;
            if (result.status == 0) {
              this.loggedIn = false;
              this.failedTitle = '登录失效';
              this.failedDetails = '请重新登录!';
              this.failedAuth = true;
            } else {
              this.loggedInInfo.uid = result.data.user_id;
              this.loggedInInfo.uname = result.data.user_name;
            }
          }).catch(err => {
            this.failedTitle = '网络错误';
            this.failedDetails = '无法连接至API服务器!';
            this.failedAuth = true;
          })
      }
    },
    logOut: function () {
      let session_data = this.getNativeLoginInfo();
      let uid = session_data[0];
      let sid = session_data[1];
      this.$cookies.remove('uid');
      this.$cookies.remove('sid');
      this.$cookies.remove('ssid');
      axios.post(`/api/user/logout?uname=${uid}&sessionid=${sid}`);
      this.verifyLogin();
    },
    logginInDialogClosed: function () {
      if (this.loggingIn) { this.$refs.loggingInDialog.show(); }
    },
    loginBtnClicked: function () {
      if (this.accountid == '' || this.pwd == '') {
        this.failedTitle = '字段为空'
        this.failedDetails = '账户ID或密码输入为空!'
        this.failedAuth = true;
      } else {
        this.doLogin(this.accountid, this.pwd);
      }
    }
  }
}
</script>
<style scoped>
.account-container>h1 {
  font-family: Consolas, Symbol, 'Microsoft Sans Serif', 'Times New Roman';
}

.account-container {

  width: calc(100% - 4px);
  height: calc(100vh - 64px);
  display: grid;
  place-content: center;
  margin: 2px;
}

h1,
h2 {
  margin: 0.25em;
  padding: 0;
}

h2 {
  text-align: start;
}

hr {
  width: 32vw;
  border-color: #cccccc55;
  margin-bottom: 1em;
}

md-outlined-text-field {
  text-align: left;
  margin-top: 1em;
}

md-filled-button {
  margin-top: 1em;
}


.loading-container {
  margin: 1em;
  display: flex;
  justify-content: center;
  align-items: center;
}

.loading-container>* {
  margin: 1em;
  font-family: Consolas, Symbol, 'Microsoft Sans Serif', 'Times New Roman';
  font-size: 16pt;
}
</style>