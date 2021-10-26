<template>
  <div>
    <!-- 搜索框 + 一些热门公司的列举 -->
    <!-- v-model绑定的值就是监听到的值 -->
    <input type="text" id="cc" placeholder="Search Company..." v-model="search_comp" />
    <div class="before-default" v-if="search_comp===''">
      <br/>
      Companies you may be interesed in...
    </div>
    <ul id="cl-show">
      <li v-for="(item) in filtered_list" :key="item.name" class='clist'>
        <router-link :to="item.url">{{ item.name + " Dashboard" }}</router-link>
      </li>
    </ul>
    <!-- <div class='cctest'>{{ "Show " + search_comp + " here" }}</div> -->
  </div>
</template>

<script>
import axios from 'axios'
export default {
  name: 'CompChoice',
  data () {
    return {
      search_comp: '',
      // filtered_list: [],
      iRawList: [], // important company list
      RawList: [] // waiting for getData() from backend
    }
  },
  methods: {
    getData () {
      var that = this
      const path = 'http://127.0.0.1:5000/comp_list'
      axios.get(path).then(function (response) {
        // 这里服务器返回的 response 为一个 json object，可通过如下方法需要转成 json 字符串
        // 可以直接通过 response.data 取key-value
        // 坑一：这里不能直接使用 this 指针，不然找不到对象
        that.RawList = {} // 这行必须要有，不然刷新的时候会因为RawList没有实质改变而不显示列表
        var msg = response.data
        // 坑二：这里直接按类型解析，若再通过 JSON.stringify(msg) 转，会得到带双引号的字串
        var index = 0
        var c = ''
        var base = '/company/'
        that.iRawList = msg.icomp_list
        that.RawList = []
        for (index in msg.comp_list) {
          c = msg.comp_list[index]
          // alert(c)
          that.RawList.push({'name': c, 'url': base + c})
        }

        // alert('Success ' + response.status + ', ' + response.data + ', ' + msg)
      }).catch(function (error) {
        alert('Error ' + error)
      })
    }
  },
  computed: {
    filtered_list: function () {
      // 根据情况过滤
      // 当搜索框为空，那么返回贡献最多的十个公司（this.icomp_list中）
      // 搜索框不为空的时候，返回开头匹配搜索框的、字母序前10的公司
      // alert("CompChoice.search_comp: " + this.search_comp) // 可以正常输出search_comp的值
      // alert(this.RawList.length)
      // alert(this.iRawList.length)
      // alert(this.filtered_list.length)
      // 坑死了!!直接用this就会显示search_comp未定义, 下面函数也只调用一次。莫名其妙不懂
      // 而且直接用this的一个现象就是，search_comp可以正常alert出，但是模板里的无法渲染（如class=cctest的div）
      var that = this
      if (that.search_comp === '') {
        return that.RawList.filter(function (item) {
          // alert('CompChoice path 1') // 如果正常工作，这个会调用跟RawList数组一样的长度
          return that.iRawList.includes(item.name)
        })
      } else {
        return that.RawList.filter(function (item) {
          // alert('CompChoice path 2') // 如果正常工作，这个会调用跟RawList数组一样的长度
          return item.name.toLowerCase().startsWith(that.search_comp)
        })
      }
    }
  },
  mounted: function () {
    // alert('openstack created')
    // alert(this.filtered_list.length)
    let that = this
    that.$nextTick(function () {
      // alert('CompChoice before get data')
      that.getData()
      // alert('CompChoice after get data')
    })
  }
}
</script>

<style scoped>
#cc {
  width: 550px;
}
.clist {
  text-align: left;
}
.cctest {
  height: 50px;
  width: 100px;
}
.before-default {
  padding-left: 20px;
  text-align: left;
}
</style>
