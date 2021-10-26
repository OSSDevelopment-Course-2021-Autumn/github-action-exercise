<template>
  <!-- 为 ECharts 准备一个具备大小（宽高）的 DOM -->
  <div class="company_network" :style="{width: '1000px', height: '600px', border: '1px solid lightgray'}"></div>
</template>

<script>
// https://codepen.io/pen/
// https://visjs.github.io/vis-network/examples/
import { DataSet, Network } from 'vis'

export default {
  name: 'CNetwork',
  data () {
    return {
      network: null
    }
  },
  props: {
    SID: String,
    Nodes: Array,
    Edges: Array
  },
  mounted: function () {
    let that = this
    that.$nextTick(function () {
      that.drawNetwork()
    })
  },
  methods: {
    drawNetwork () {
      let that = this
      // alert(typeof (that.Edges))
      // alert(JSON.stringify(that.Edges))
      // create an array with nodes
      var nodes = new DataSet(that.Nodes)
      // create an array with edges
      var edges = new DataSet(that.Edges)
      // create a network
      var container = document.getElementById(that.SID)
      var data = {
        nodes: nodes,
        edges: edges
      }
      var options = {
        nodes: {
          shape: 'dot' // 节点形状：圆形，字位于节点下方
        },
        edges: {
          font: {
            color: '#696969',
            size: 10
          }
        }
      }
      that.network = new Network(container, data, options)
    }
  }
}
</script>

<style scoped>
</style>
