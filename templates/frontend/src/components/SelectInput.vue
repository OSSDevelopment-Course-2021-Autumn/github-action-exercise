<template>
  <div>
    <div class="title">
      <input type="text" placeholder="请选择想对比的公司" v-model="select_con" @click.stop="liShow" />
      <i class="icon" @click.stop="liShow">∨</i>
    </div>
    <ul v-show="isShow" @click.stop="liShow">
      <li v-for="item in candidateCompany" :key="item.Id">
        <label :id="item.Id">
          <input type="checkbox" v-model="item.Check"/>
          {{item.Name}}
        </label>
      </li>
    </ul>
  </div>
</template>

<script>
export default {
// 参考： https://www.jianshu.com/p/bebb943db4a6
  name: 'SelectInput',
  props: {
    candidateCompany: Array
  },
  data () {
    return {
      checked_companys: [], // 被选中的用于对比的公司
      isShow: false, // 下拉列表是否显示
      select_con: ''// 被选中的内容
    }
  },
  methods: {
    liShow () {
      this.isShow = true
    }
  },
  mounted () {
    let that = this
    // 点击页面空白处隐藏下拉列表
    document.addEventListener('click', function () {
      that.isShow = false
    })
  },
  watch: {
    candidateCompany: {
      handler (newVal, oldVal) {
        // 选中数据
        this.checked_companys = newVal.filter(function (item) {
          return item.Check === true
        })
        // 在页面打印出的数据
        this.selectCon = '' // 点击的当前项的展示
        for (var i = 0; i < this.checked_companys.length; i++) {
          this.selectCon += this.checked_companys[i].Name + '  '
        }
        // 给父组件传值
        this.$emit('change', this.selectCon)
        // alert(this.selectCon)// 这个会弹出正确selectCon的值，所以勾选checkbox之后的确会调用handler
      },
      deep: true
    }
  }
}
</script>

<style scoped>
.selectInput .title {
  width: 300px;
  position: relative;
}
.selectInput input[type="text"] {
  width: 300px;
  height: 40px;
  padding: 0 5px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  border-radius: 3px;
  -moz-border-radius: 3px; /* Firefox */
  -webkit-border-radius: 3px; /* Safari 和 Chrome */
  border-radius: 3px; /* Opera 10.5+, 以及使用了IE-CSS3的IE浏览器 */
}
.selectInput i {
  position: absolute;
  width: 30px;
  height: 40px;
  line-height: 38px;
  right: -12px;
  top: 1px;
  text-align: center;
  cursor: pointer;
}
.selectInput ul {
  border-radius: 3px;
  -moz-border-radius: 3px; /* Firefox */
  -webkit-border-radius: 3px; /* Safari 和 Chrome */
  border-radius: 3px; /* Opera 10.5+, 以及使用了IE-CSS3的IE浏览器 */
  box-shadow: 0 1px 6px rgba(0, 0, 0, 0.2);
  -moz-box-shadow: 0 1px 6px rgba(0, 0, 0, 0.2); /* Firefox */
  -webkit-box-shadow: 0 1px 6px rgba(0, 0, 0, 0.2); /* Safari 和 Chrome */
  box-shadow: 0 1px 6px rgba(0, 0, 0, 0.2); /* Opera 10.5+, 以及使用了IE-CSS3的IE浏览器 */
  width: 253px;
  /* border: 1px solid #ccc; */
  padding: 10px 30px;
  text-align: left;
}
.selectInput li {
  line-height: 30px;
}
</style>
