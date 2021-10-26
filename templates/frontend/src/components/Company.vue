<template>
  <div>
    <div class='text-block'>
      <div class="intro">
        <p> Company:  <span class="attr">{{ "  " + company_name}}</span></p>
      </div>
      <div class="intro" v-if="company_type">
        <p> Company Type:  <span class="attr">{{ "  " + company_type }}</span></p>
      </div>
    </div>
    <div class="center-block" style=padding-top:150px>
      <div style=float:left;padding-left:250px;padding-right:20px :style="{width: '440px', height: '360px'}">
        <PieGraph v-if="flag" id='comp-chart1' :SID="sid1" :PCTitle="title1" :Data="data1" :style="{width: '400px', height: '300px'}" >
        </PieGraph>
      </div>
      <div style=float:left;padding-left:100px;padding-right:20px :style="{width: '440px', height: '360px'}">
        <PieGraph v-if="flag" id='comp-chart2' :SID="sid2" :PCTitle="title2" :Data="data2" :style="{width: '400px', height: '300px'}" >
        </PieGraph>
      </div>
    </div>
    <div style=position:absolute;left:10px;top:700px;>
      <div style=float:left;padding-left:20px;padding-right:20px :style="{width: '150px', height: '500px'}">
        <SelectInput :candidateCompany="candidate_company" @change="change"></SelectInput>
        <span>selected: <b>{{select_company}}</b></span>
      </div>
      <div style=float:left;padding-left:100px;padding-right:20px :style="{width: '440px', height: '360px'}">
        <LineChart v-if="flag" id='intensity-chart' :SID="intensity_id" :Meaning="intensity_meaning" :Xdata="xintensity_data" :Series="yintensity_series" :style="{width: '400px', height: '300px'}"></LineChart>
      </div>
      <div style=float:left;padding-left:100px;padding-right:20px :style="{width: '440px', height: '360px'}">
        <LineChart v-if="flag" id='extent-chart' :SID="extent_id" :Meaning="extent_meaning" :Xdata="xextent_data" :Series="yextent_series" :style="{width: '400px', height: '300px'}"></LineChart>
      </div>
    </div>
    <div style=position:absolute;left:200px;top:1000px;>
      <div style=float:left;padding-left:100px;padding-right:20px :style="{width: '440px', height: '360px'}">
        <LineChart v-if="flag" id='commit-state-chart' :SID="commit_state_id" :Meaning="commit_state_meaning" :Xdata="xcommit_state_data" :Series="ycommit_state_series" :style="{width: '400px', height: '300px'}"></LineChart>
      </div>
    </div>
    <div style=position:absolute;left:200px;top:1400px;>
      <div style=float:left;padding-left:100px;padding-right:20px :style="{width: '1100px', height: '650px'}">
        <CNetwork v-if="flag" id='network' :SID="network_id" :Nodes="nodes" :Edges="edges" :style="{width: '1000px', height: '600px'}"></CNetwork>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import PieGraph from './PieGraph'
import LineChart from './LineChart'
import SelectInput from './SelectInput'
import CNetwork from './CNetwork'
import qs from 'qs'

export default {
  name: 'Company',
  data () {
    return {
      company_name: '',
      company_type: '',
      sid1: '',
      sid2: '',
      intensity_id: '',
      extent_id: '',
      commit_state_id: '',
      network_id: '',
      title1: '',
      title2: '',
      title3: '',
      intensity_meaning: '',
      extent_meaning: '',
      commit_state_meaning: [],
      xintensity_data: [],
      xextent_data: [],
      xcommit_state_data: [],
      yintensity_series: [],
      yextent_series: [],
      ycommit_state_series: [],
      flag: false,
      candidate_company: [// 备选公司数据
        {
          Id: 0,
          Name: 'Canonical',
          Check: false
        },
        {
          Id: 1,
          Name: 'Huawei',
          Check: false
        },
        {
          Id: 2,
          Name: 'HP',
          Check: false
        },
        {
          Id: 3,
          Name: 'HPE',
          Check: false
        },
        {
          Id: 4,
          Name: 'IBM',
          Check: false
        },
        {
          Id: 5,
          Name: 'Intel',
          Check: false
        },
        {
          Id: 6,
          Name: 'Mirantis',
          Check: false
        },
        {
          Id: 7,
          Name: 'NEC',
          Check: false
        },
        {
          Id: 8,
          Name: 'Rackspace',
          Check: false
        },
        {
          Id: 9,
          Name: 'Red Hat',
          Check: false
        }
      ],
      select_company: '',
      nodes: [],
      edges: []
    }
  },
  methods: {
    getData () {
      var that = this
      that.company_name = this.$route.params.comp_name
      // alert(that.company_name)
      const path = 'http://127.0.0.1:5000/company/' + this.company_name
      let args = {'company': this.company_name, 'compared_company': this.select_company}
      axios.post(path, qs.stringify(args)).then(function (response) {
        // 这里服务器返回的 response 为一个 json object，可通过如下方法需要转成 json 字符串
        // 可以直接通过 response.data 取key-value
        // 坑一：这里不能直接使用 this 指针，不然找不到对象
        var msg = response.data
        // 坑二：这里直接按类型解析，若再通过 JSON.stringify(msg) 转，会得到带双引号的字串
        // that.company_intro = msg.test // 测试输出用而已

        that.company_type = msg.comp_type

        that.sid1 = 'comp-chart1'
        that.data1 = msg.repo2amount
        that.title1 = 'Company Repository Type Preference'
        that.sid2 = 'comp-chart2'
        that.data2 = msg.task2amount
        that.title2 = 'Company Task Type Preference'

        that.intensity_id = 'intensity-chart'
        that.extent_id = 'extent-chart'
        that.commit_state_id = 'commit-state-chart'
        that.network_id = 'network'

        that.xintensity_data = msg.month_list
        that.xextent_data = msg.month_list
        that.xcommit_state_data = msg.month_list_main
        that.yintensity_series = new Array(0)
        that.yextent_series = new Array(0)
        that.ycommit_state_series = new Array(0)
        that.intensity_meaning = new Array(0)
        that.extent_meaning = new Array(0)
        that.commit_state_meaning = ['Commit Timeline']

        var idata = new Array(0)
        var edata = new Array(0)
        for (let comp in msg.month_state) {
          let compInfo = msg.month_state[comp]
          idata = new Array(0)
          edata = new Array(0)
          that.intensity_meaning.push(comp + '贡献强度')
          that.extent_meaning.push(comp + '贡献广度')
          for (let ci in compInfo) {
            let compMonthInfo = compInfo[ci]
            idata.push(compMonthInfo['intensity_rel_cmt'])
            edata.push(compMonthInfo['extent_rel_r'])
          }
          that.yintensity_series.push({
            name: comp + '贡献强度',
            type: 'line',
            data: idata
          })
          that.yextent_series.push({
            name: comp + '贡献广度',
            type: 'line',
            data: edata
          })
        }
        that.ycommit_state_series.push({
          name: 'Commit Timeline',
          type: 'line',
          data: msg.commit_state
        })
        that.nodes = msg['nodes']
        that.edges = msg['edges']
        that.flag = true
        // alert('Success ' + response.status + ', ' + response.data + ', ' + msg)
      }).catch(function (error) {
        alert('Error ' + error)
      })
    },
    change (msg) {
      let that = this
      that.select_company = msg
      that.getData()
    }
  },
  components: {
    PieGraph,
    LineChart,
    SelectInput,
    CNetwork
  },
  created: function () {
    // alert('company created')
    // alert(this.filtered_list.length)
    let that = this
    that.flag = false
    that.$nextTick(function () {
      // alert('company before get data')
      that.getData()
      // alert('company after get data')
    })
  }
}
</script>

<style scoped>
.center-block {
  margin: 0 auto;
}
.text-block {
  padding-left: 300px;
  margin: 0 auto;
}
.intro {
  font-weight: bold;
  width: 600px;
  float: left;
  text-align: left;
  font-size: 20px;
  font-family: Tahoma;
  height: 40px;
}
.attr {
  font-family: "Hiragino Sans GB";
  font-weight: normal;
}
</style>
