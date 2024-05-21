<template>
  <div class="cards-container" v-if="games.length > 0">
    <div class="card-container" v-for="game in games" :key="game.id"
      :style="'background-image: url(' + game.game_img + ')'">
      <p class="card-title">
        {{ game.game_name }}
      </p>
      <span></span>
      <div class="card-inner-field">
        <md-chip-set>
          <md-assist-chip v-for="tag in game.game_tags.sort((a, b) => a.length - b.length).slice(0,2)" :key="tag.id" :label="tag" :href="'/?tag='+tag">
          </md-assist-chip>
        </md-chip-set>
        <span></span>
        <a :href="game.game_href">browse details &gt;&gt;</a>
      </div>
    </div>
  </div>
  <div class="error" v-if="games.length <= 0">no results</div>
</template>
<style scoped>
.cards-container {
  width: calc(100% - 2em);
  max-width: 1440px;
  display: flex;
  justify-content: center;
}
.cards-container {
  display: flex;
  flex-wrap: wrap;
  overflow: hidden;
}

.card-container {
  display: inline-block;
  padding: 0.5em;
  margin: 0.5em;
  overflow: hidden;
  height: 6em;
  width: 14em;
  background-color: #ccc;
  display: flex;
  flex-direction: column;
  background-size:contain ;
}

.card-container span {
  flex-grow: 1;
}

.card-container>p {
  width: 100%;
  overflow: hidden;
  text-overflow: ellipsis;
  color: #fff;
  text-shadow: 1px 1px 5px #000;
  margin: 0;
  margin-top: 0.5em;
  padding: 0.1em 0;
  max-height: 2.5em;
}

.card-container>.card-inner-field {
  background-color: #eeeeeeee;
  display: flex;
  flex-direction: column;
  margin: -0.5em;
  padding: 0.5em;
  color: #000;
  height: 0;
  overflow: scroll;
  overflow-x: hidden;
  opacity: 0;
  z-index: 999;
}

.card-container:hover>.card-inner-field {
  opacity: 1;
  height: 3.5em;
  transition: all ease-in-out 0.2s;
}

.card-container .card-title {
  position: relative;
  bottom: 0;
}
md-assist-chip {
  --md-assist-chip-label-text-size:10pt;
}
.card-inner-field a{
  text-decoration: none;
  outline: none;
  color: var(--md-sys-color-primary);
  font-weight: bold;
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
<script>
export default {
  name: 'GameList',
  props: {
    games: Array
  }
}
</script>