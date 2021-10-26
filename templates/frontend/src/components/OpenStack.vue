<template>
  <div>
    <div class="intro">
      <div>-Company Dashboard will help you know company's features (Repository Preferences/Task Preferences)</div>
      <div>-Company Dashboard will show you statistics of company's activities (Contribution/Repository selection over time)</div>
      <br/>
    </div>
    <div class="center-block">
      <div style=float:left;padding-left:20px;padding-right:20px :style="{width: '400px', height: '360px'}">
        <PieGraph v-if="flag" id='pc1' :SID="sid1" :PCTitle="title1" :Data="data1" :style="{width: '440px', height: '300px'}" >
        </PieGraph>
      </div>
      <div style=float:left;padding-left:20px;padding-right:20px :style="{width: '400px', height: '360px'}">
        <PieGraph v-if="flag" id='pc2' :SID="sid2" :PCTitle="title2" :Data="data2" :style="{width: '440px', height: '300px'}" >
        </PieGraph>
      </div>
      <div style=float:left;padding-left:20px;padding-right:20px :style="{width: '400px', height: '360px'}">
        <PieGraph v-if="flag" id='pc3' :SID="sid3" :PCTitle="title3" :Data="data3" :style="{width: '400px', height: '300px'}" >
        </PieGraph>
      </div>
      <div class="cc">
        <!-- 提供一些默认的公司选项；最好能根据搜索框进行链接更改 -->
        <CompChoice></CompChoice>
      </div>
    </div>
  </div>
</template>

<script>
// import Vue from 'vue'
import axios from 'axios'
import PieGraph from './PieGraph'
import CompChoice from './CompChoice'

export default {
  name: 'OpenStack',
  data () {
    return {
      // rd: -1,
      serverResponse: '',
      sid1: '',
      sid2: '',
      sid3: '',
      title1: '',
      title2: '',
      title3: '',
      data1: {},
      data2: {},
      data3: {},
      flag: false
    }
  },
  methods: {
    getData () {
      var that = this
      const path = 'http://127.0.0.1:5000/home'
      axios.get(path).then(function (response) {
        // 这里服务器返回的 response 为一个 json object，可通过如下方法需要转成 json 字符串
        // 可以直接通过 response.data 取key-value
        // 坑一：这里不能直接使用 this 指针，不然找不到对象
        var msg = response.data
        // 坑二：这里直接按类型解析，若再通过 JSON.stringify(msg) 转，会得到带双引号的字串
        that.serverResponse = msg

        that.sid1 = 'pc1'
        that.sid2 = 'pc2'
        that.sid3 = 'pc3'

        that.title1 = 'OpenStack Company Goals Distribution'
        that.title2 = 'OpenStack Repository Types Distribution'
        that.title3 = 'OpenStack Task Amounts Distribution'

        that.data1 = msg.ct2amount
        that.data2 = msg.rt2amount
        that.data3 = msg.task2amount

        that.flag = true

        // that.rd = msg.rd

        // alert('Success ' + response.status + ', ' + response.data + ', ' + msg)
      }).catch(function (error) {
        alert('Error ' + error)
      })
    }
  },
  components: {
    PieGraph,
    CompChoice
  },
  created: function () {
    // alert('openstack created')
    let that = this
    that.flag = false
    that.$nextTick(function () {
      // alert('before get data')
      that.getData()
      // alert('after get data')
    })
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.center-block {
  margin: 0 auto;
}
.cc {
  margin: 0 auto;
  width: 600px;
}
.intro {
  text-align: left;
  padding-left: 60px;
  font-size: large;
}
</style>
