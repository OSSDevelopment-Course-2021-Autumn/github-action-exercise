<template>
  <div id="app">
    <div id="Title">
      <h1>Welcome to Company Dashboard!</h1>
    </div>
    <router-view/>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 5px;
}
#Title {
  font-size: x-large;
  color: #ffffff;
  background: #ff2200;
  font-family: "Comic Sans MS", cursive, sans-serif
}
</style>
