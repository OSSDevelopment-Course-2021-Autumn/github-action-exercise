<template>
    <!-- 为 ECharts 准备一个具备大小（宽高）的 DOM -->
    <div id="chartLine" class="line-wrap" :style="{width: '400px', height: '300px'}"></div>
</template>

<script>
import * as echarts from 'echarts'
require('echarts/theme/shine')// 引入主题
export default {
  name: 'LineChart',
  data () {
    return {
      chartLine: null
    }
  },
  props: {
    SID: String,
    Xdata: Array,
    Meaning: Array,
    Series: Array
  },
  mounted: function () {
    let that = this
    that.$nextTick(function () {
      that.drawLineChart()
    })
  },
  methods: {
    drawLineChart () {
      var that = this
      // alert('From LineChart')
      // alert(that.Xdata.length)
      // alert(that.Ydata.length)
      that.chartLine = echarts.init(document.getElementById(that.SID), 'shine')// 基于准备好的dom，初始化echarts实例
      let option = {
        tooltip: {
          trigger: 'axis'
        },
        legend: {
          data: that.Meaning
        },
        calculable: true,
        xAxis: [
          {
            type: 'category',
            boundaryGap: false,
            axisTick: {
              show: false
            },
            data: that.Xdata// 月份
          }
        ],
        yAxis: [
          {
            type: 'value',
            axisTick: {
              show: false
            },
            name: ''// y轴含义
          }
        ],
        series: that.Series
      }
      // 使用刚指定的配置项和数据显示图表
      this.chartLine.setOption(option)

      // alert(typeof(that.Series))
    }
  },
  watch: {
    Series: {
      handler (newVal, oldVal) {
        let that = this
        that.chartLine.clear()// 清空本组件的图标, 不然上次页面的数据会残留
        that.drawLineChart()
      },
      deep: true
    }
  }
}
</script>

<style scoped>
</style>
