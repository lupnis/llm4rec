<template>
  <div class="aiview">
    <header>
      <md-text-button href="/">主页</md-text-button>
      <md-filled-button href="/ai">AI对话搜索</md-filled-button>
      <span></span>
      <md-text-button href="/account">切换账户</md-text-button>
    </header>
    <h1 v-if="loggedIn">已登录
      <md-filled-button @click="this.createChat()">新建会话</md-filled-button>
    </h1>
    <h1 v-else>未登录</h1>
    <hr />
    <div class="chat-container" ref="chatContainer" v-if="loggedIn && inSession">
      <div :class="{ 'chat-chat': true, 'chat-left': index % 2 == 0, 'chat-right': index % 2 == 1 }"
        v-for="(item, index) in history" :key="index">
        <md-icon v-if="index % 2 == 0">robot</md-icon>
        <div class="content-container">
          {{ item }}
        </div>
        <md-icon v-if="index % 2 == 1">people</md-icon>
      </div>
      <div class="chat-chat chat-processing" v-if="processing"><md-circular-progress four-color indeterminate></md-circular-progress>处理中...</div>
    </div>
    <div class="prompt-container" v-if="loggedIn && inSession">
      <md-outlined-text-field placeholder="输入文字开始聊天" rows="2" type="textarea" v-bind:disabled="processing"
        :value="prompt" @input="event => prompt = event?.target?.value" @keydown.enter="sendChat">
      </md-outlined-text-field>
      <md-icon-button @click="sendChat" v-bind:disabled="processing"><md-icon>send</md-icon></md-icon-button>
    </div>
    <md-dialog ref="creatingDialog" type="alert" @closed="creatingDialogClosed">
      <div slot="headline">大模型初始化</div>
      <form slot="content">
        <div class="loading-container">
          <md-circular-progress four-color indeterminate></md-circular-progress>
          <a> {{ creatingText }}</a>
        </div>
      </form>
    </md-dialog>
  </div>
</template>

<script>
import axios from 'axios';
export default {
  name: "AIView",
  data() {
    return {
      loggedIn: false,
      uid: "未登录",
      creatingSession: false,
      creatingText: '',
      inSession: false,
      processing: false,
      history: ['Hi! How can I assist you today?'],
      prompt: ''
    }
  },
  watch: {
    history: {
      deep: true,
      handler(nv) {
        this.autoScroll();
      }
    },
    creatingSession(nv) {
      if (nv) {
        this.$refs.creatingDialog.show();
      } else {
        this.$refs.creatingDialog.close();
      }
    }
  },
  mounted() {
    this.verifyLogin();
    this.loadChat();
  },
  methods: {
    creatingDialogClosed: function () {
      if (this.creatingSession) { this.$refs.creatingDialog.show(); }
    },
    autoScroll: function () {
      if (this.loggedIn == false || this.inSession == false) {
        return;
      }
      this.$nextTick(() => {
        const container = this.$refs.chatContainer;
        container.scrollTo({ top: container.scrollHeight, behavior: 'smooth' });
      });
    },
    getNativeLoginInfo: function () {
      let uid = this.$cookies.get('uid');
      let sid = this.$cookies.get('sid');
      return [uid, sid];
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
            let result = resp.data;
            if (result.status == 0) {
              this.loggedIn = false;
            } else {
              this.loggedIn = true;
              this.uid = uid;
            }
          }).catch(err => {
            this.loggedIn = false;
          });
      }
    },
    createChat: function () {
      this.creatingText = '[0/3]会话准备中...';
      this.creatingSession = true;
      if (this.inSession == true) {
        this.creatingText = '[1/3]销毁上次会话...';
        this.destoryChat();
      }
      this.creatingText = '[2/3]创建新会话...';
      this.creatingText = '[3/3]载入用户偏好...';
      let session_data = this.getNativeLoginInfo();
      let uid = session_data[0];
      let sid = session_data[1];
      axios.post(`/api/chat/create?uname=${uid}&sessionid=${sid}`)
        .then(resp => {
          let result = resp.data;
          if (result.status == 0) {
            this.loggedIn = false;
          } else {
            this.$cookies.set("ssid", result.data);
            this.creatingSession = false;
            this.creatingText = '';
            this.inSession = true;
            this.processing = false;
          }
        }).catch(err => {
          this.loggedIn = false;
        });
    },
    destoryChat: function () {
      let session_data = this.getNativeLoginInfo();
      let uid = session_data[0];
      let sid = session_data[1];
      let ssid = this.$cookies.get('ssid');
      this.$cookies.remove('ssid');
      this.inSession = false;
      this.history = ['Hi! How can I assist you today?'];
      axios.post(`/api/chat/stop?uname=${uid}&sessionid=${sid}&chat_sessionid=${ssid}`);
    },
    loadChat: function () {
      let ssid = this.$cookies.get('ssid');
      axios.get(`/api/chat/history?chat_sessionid=${ssid}`)
        .then(resp => {
          let result = resp.data;
          if (result.status == 0) {
            this.inSession = false;
          } else {
            let history_r = ['Hi! How can I assist you today?', ...result.slice(6, result.length)];
            this.inSession = true;
            this.history = history_r;
          }
        }).catch(err => {
          this.inSession = false;
        });
    },
    sendChat: function () {
      let ssid = this.$cookies.get('ssid');
      let prompt = this.prompt;
      if (prompt == '') {
        return;
      }
      this.history.push(prompt);
      this.processing = true;
      this.prompt = '';
      axios.post(`/api/chat/chat?chat_sessionid=${ssid}&content=${prompt}`)
        .then(resp => {
          let result = resp.data;
          this.processing = false;
          if (result.status == 0) {
            this.inSession = false;
          } else {
            this.history.push(result.answer);
          }
        }).catch(err => {
          this.inSession = false;
        });
    }
  }
}
</script>
<style scoped>
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

md-filled-tonal-button {
  --md-filled-tonal-button-label-text-color: #fff;
  --md-filled-tonal-button-container-shape: 5px;
}

md-filled-tonal-button svg {
  color: #fff;
}

.chat-container .chat-processing {
  background-color: #eeeeee;
  padding: 0.75em;
  margin: 2em 10em !important;
  border-radius: 10px;
}


h1 {
  font-family: Consolas, Symbol, 'Microsoft Sans Serif', 'Times New Roman';
}

.chat-container {
  width: calc(100% - 4px);
  margin: 2px;
  height: calc(100vh - 250px);
  flex-grow: 1;
  overflow: auto;
  overflow-x: hidden;
  display: flex;
  flex-direction: column;
}

.chat-container .chat-chat {
  margin: 0.5em;
}

.chat-left,
.chat-right {
  display: grid;
  padding: 0.5em;
}

.chat-left {
  margin-right: 10em !important;
  grid-template-columns: 50px auto;
  justify-content: start;
}

.chat-right {
  margin-left: 10em !important;
  grid-template-columns: auto 50px;
  justify-content: end;
}

.chat-left>img,
.chat-left>md-icon {
  margin-right: 1em;
  width: 32px;
  height: 32px;
}

.chat-right>img,
.chat-right>md-icon {
  margin-left: 1em;
  width: 32px;
  height: 32px;
}

.content-container {
  border-radius: 10px;
  padding: 0.5em 1em;
  text-align: justify;
  line-height: 1.5em;
}

.content-container p {
  margin-top: 0.5em;
  margin-bottom: 0.5em;
  padding: 0;
}

.chat-right>.content-container {
  background-color: #ffcc00;
}

.chat-left>.content-container {
  background-color: #85ff33;
}

.prompt-container {
  margin-top: 1em;
  height: 5em;
  bottom: 0;
  width: calc(100vw -10px);
  display: grid;
  grid-template-columns: 1fr 50px;
  align-items: center;
}

.prompt-container md-icon-button {
  margin-left: 5px;
}

.prompt-container md-outlined-text-field {
  resize: none;
}


::-webkit-scrollbar {
  width: 5px;
}

::-webkit-scrollbar:focus {
  width: 10px;
}

/* Track */
::-webkit-scrollbar-track {
  background: #f1f1f1;
}

/* Handle */
::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 5px;
}

/* Handle on hover */
::-webkit-scrollbar-thumb:hover {
  background: #555;
}
</style>