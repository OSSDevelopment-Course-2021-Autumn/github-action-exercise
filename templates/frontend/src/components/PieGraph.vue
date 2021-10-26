<template>
  <div>
    <span class='pie-wrap' :style="{width: '400px', height: '300px'}"><slot></slot></span>
  </div>
</template>

<script>
import echarts from 'echarts'
require('echarts/theme/macarons') // theme
export default {
  name: 'PieGraph',
  props: {
    SID: String,
    PCTitle: String,
    Data: Object
  },
  data () {
    return {
      chartPie: '',
      mydata: ''
    }
  },
  mounted: function () {
    let that = this
    that.$nextTick(function () {
      var labelArr = new Array(Object.keys(this.Data).length)
      var valueArr = new Array(Object.keys(this.Data).length)
      var objArr = new Array(Object.keys(this.Data).length)
      for (let key in this.Data) {
        labelArr.push(key)
        valueArr.push(this.Data[key])
        objArr.push({'value': this.Data[key], 'name': key})
      }
      this.$session.set('SID', this.SID)
      this.$session.set('labelArr', labelArr)
      this.$session.set('valueArr', valueArr)
      this.$session.set('objArr', objArr)
      // alert('in mounted')
      that.drawPieChart()
    })
  },
  methods: {
    drawPieChart () {
      let mytextStyle = {
        color: '#333',
        fontSize: 18
      }
      let mylabel = {
        show: true,
        position: 'right',
        offset: [30, 40],
        formatter: '{b} : {c} ({d}%)'
      }

      var sid = this.$session.get('SID')
      // alert(sid)
      var labelArr = this.$session.get('labelArr')
      // var valueArr = this.$session.get('valueArr')
      var objArr = this.$session.get('objArr')
      this.chartPie = echarts.init(document.getElementById(sid), 'macarons')

      // alert(document.getElementById(sid).innerHTML + "\nIn case it's null")
      this.chartPie.setOption({
        title: {
          text: this.PCTitle,
          // subtext: '纯属虚构',
          x: 'center'
        },
        tooltip: {
          // trigger: 'item',
          // fomatter: '{a} <br/>{b} : {c} ({d}%)',
          textStyle: mytextStyle
        },
        legend: {
          data: labelArr,
          left: 'center',
          top: 'bottom',
          orient: 'horizontal'
        },
        series: [
          {
            name: 'Type',
            type: 'pie',
            radius: ['20%', '30%'],
            center: ['50%', '35%'],
            data: objArr,
            animationEasing: 'cubicInOut',
            animationDuration: 1500,
            label: {
              emphasis: mylabel
            }
          }
        ]
      })
    }
  }
}
</script>

<style>

</style>
