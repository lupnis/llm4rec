<template>
  <div>
    <header>
      <md-filled-button href="/">主页</md-filled-button>
      <md-text-button href="/ai">AI对话搜索</md-text-button>
      <span></span>
      <md-text-button href="/account">切换账户</md-text-button>
    </header>
    
    <div class="searchbox-container">
      <md-outlined-text-field 
      placeholder="常规搜索..." 
      :value="searchText" 
      @input="event => searchText = event?.target?.value" 
      @keydown.enter="search">
        <md-text-button></md-text-button>
        <md-icon slot="leading-icon" @click="search">search</md-icon>
      </md-outlined-text-field>
    </div>


    <div class="loading-container" v-if="!loggedIn">
      <md-circular-progress four-color indeterminate></md-circular-progress>
      <a>{{ pendingLoginText }}</a>
    </div>
    <div class="loading-container" v-if="loggedIn && loading">
      <md-circular-progress four-color indeterminate></md-circular-progress>
      <a>{{ loadingText }}</a>
    </div>
    <div class="result-container">
      <GameList :games="recomm" />
    </div>
  </div>
</template>
<style scoped>
.searchbox-container {
  width: 100%;
  margin: 0.25em;
}

.searchbox-container>* {
  width: calc(100% - 2em);
  max-width: 1024px;
  text-align: start;
}

md-icon {
  cursor: pointer;
}

.loading-container {
  width: 100%;
  margin: 0.25em;
  display: flex;
  justify-content: center;
  align-items: center;
}

.loading-container>* {
  margin: 1em;
  font-family: Consolas, Symbol, 'Microsoft Sans Serif', 'Times New Roman';
  font-size: 16pt;
}

.result-container {
  width: 100%;
  margin: 0.25em;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}
</style>
<script>
import GameList from '@/components/GameList.vue'
import axios from 'axios';
export default {
  name: 'HomeView',
  components: {
    GameList
  },
  data() {
    return {
      loggedIn: false,
      pendingLoginText: "等待用户登录...",
      loading: true,
      loadingText: "正在连接至LLM服务器...",
      recomm: [],
      searchText:''
    }
  },
  mounted() {
    this.verifyLogin();
  },
  watch: {
    loggedIn(nv) {
      if (nv == true) {
        this.getRecomm();
      }
    }
  },
  methods: {
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
            }
          }).catch(err => {
            this.loggedIn = false;
          })
      }
    },
    getRecomm: function () {
      this.recomm = [];
      this.loading = true;
      let session_data = this.getNativeLoginInfo();
      let uid = session_data[0];
      let sid = session_data[1];
      axios.post(`/api/game/recommend?uname=${uid}&sessionid=${sid}&top_k=18`)
        .then(resp => {
          let result = resp.data;
          if (result.status == 0) {
            this.loggedIn = false;
          } else {
            this.recomm = result.data;
            this.loading = false;
          }
        }).catch(err => {
          this.loggedIn = false;
        });

    },
    search: function() {
      if(this.searchText==''){
        this.getRecomm();
        return;
      }
      axios.post(`/api/game/search?game_name=${this.searchText}&top_k=18`)
        .then(resp => {
          let result = resp.data;
          if (result.status == 0) {
            //
          } else {
            this.recomm = result.data;
          }
        }).catch(err => {
          this.recomm = [];
        });
    }
  }

}
</script>
