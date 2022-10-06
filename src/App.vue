<template>

  <div class="container-fluid">
    <!-- PwC logo -->
    <div class="row">
      <div class="col">
        <div style="margin-top:20px;">
          <img src="./PwC.png" style="width: 100px;">
        </div>
      </div>
    </div>

    <!-- 主要內容 -->
    <div class="row">
      <div class="col">
        <!-- 第一步 -->
        <div class="card" style="margin-top:10px;">
          <div class="card-header d-flex justify-content-between align-items-center"><b>Step1：請選擇PDF檔案：</b></div>
          <div class="card-body" style="overflow-x:auto;">
            <label for="exampleFormControlInput1" class="form-label"><b>
                <BIconFiles style="vertical-align:text-top;" class="icon" />本元件將所連結之PDF檔進行特定角度的翻轉。
              </b></label>
              <ayx data-ui-props='{type:"FileBrowse", widgetId:"pdf_path", browseType:"File"}'></ayx>
          </div>
        </div>

        <!-- 第二步 -->
        <div class="card" style="margin-top:10px;">
          <div class="card-header d-flex justify-content-between align-items-center"><b>Step2：請輸入旋轉角度：</b></div>
          <div class="card-body" style="overflow-x:auto;">
            <label for="exampleFormControlInput1" class="form-label"><b>
                <BIconColumns style="vertical-align:text-top;" class="icon" /> 選擇角度
              </b></label>
            <select class="form-control" v-model="rotate_angle">
              <option v-for="item,index in angle_list" v-bind:key="index">{{item}}</option>
            </select>
          </div>
        </div>

        <!-- 第三步 -->
        <div class="card" style="margin-top:10px;">
          <div class="card-header d-flex justify-content-between align-items-center"><b>Step2：請輸入頁數：</b></div>
          <div class="card-body" style="overflow-x:auto;">
            <label for="exampleFormControlInput1" class="form-label"><b>
                <BIconColumns style="vertical-align:text-top;" class="icon" /> 跨頁數請用","分隔，如:1,3,5。 某範圍頁數可用 "-" 表示，如:1-3。
                亦可搭配使用，如:1-3,5,7
              </b></label>
            <input type="text" class="form-control" placeholder="輸入頁數" v-model="pdf_page">
          </div>
        </div>

      </div>
    </div>
  </div>

  <footer class="footer mt-auto">
    <p class="text-muted" style="margin: 0px;text-align: center;">版本：1.0.0</p>
  </footer>

</template>
<script>

//replaceAll Polyfill

/**
 * String.prototype.replaceAll() polyfill
 * https://gomakethings.com/how-to-replace-a-section-of-a-string-with-another-one-with-vanilla-js/
 * @author Chris Ferdinandi
 * @license MIT
 */
if (!String.prototype.replaceAll) {
  String.prototype.replaceAll = function (str, newStr) {

    // If a regex pattern
    if (Object.prototype.toString.call(str).toLowerCase() === '[object regexp]') {
      return this.replace(str, newStr);
    }

    // If a string
    return this.replace(new RegExp(str, 'g'), newStr);

  };
}

//Clean Punctuation
String.prototype.clsPunc = function () {
  return this.replace(/[\p{P}\p{S}\p{Z}]/gu, '').toLowerCase()
}


export default {
  name: 'files',
  data() {
    return {
      pdf_page: "",
      rotate_angle: "",
      str_columns: [],
      val_columns: [],
      angle_list: [
        90,
        180,
        270,
      ]
    }
  },
  components: {

  },
  watch: {
    rotate_angle: {
      handler(val) {
        if (typeof window.Alteryx !== 'undefined') {
          window.Alteryx.Gui.Manager.getDataItem("rotate_angle").setValue(val)
        }
      },
      deep: true
    },
    pdf_page: {
      handler(val) {
        if (typeof window.Alteryx !== 'undefined') {
          window.Alteryx.Gui.Manager.getDataItem("pdf_page").setValue(val)
        }
      },
      deep: true
    },
    // pdf_path:{
    //   handler(val) {
    //     if (typeof window.Alteryx !== 'undefined') {
    //       window.Alteryx.Gui.Manager.getDataItem("pdf_path").setValue(val)
    //     }
    //   },
    //   deep: true
    // }
  },
  mounted() {
    if (typeof window.Alteryx !== 'undefined') {
      //Load Alteryx Library
      document.write('<link rel="import" href="' + window.Alteryx.LibDir + '2/lib/includes.html">');
      let libpath = window.Alteryx.LibDir + "2/lib/build/designerDesktop.bundle.js"
      let script = document.createElement('script')
      script.setAttribute('src', libpath)
      //Script Onload Callback
      script.onload = function () {
        //Define DataItem
        window.Alteryx.Gui.BeforeLoad = function (manager, AlteryxDataItems) {
          var rotate_angle = new AlteryxDataItems.SimpleString('rotate_angle')
          manager.addDataItem(rotate_angle)
          var pdf_page = new AlteryxDataItems.SimpleString('pdf_page')
          manager.addDataItem(pdf_page)
          var pdf_path = new AlteryxDataItems.SimpleString('pdf_path')
          manager.addDataItem(pdf_path)
          // Bind to Checkbox widget
          manager.bindDataItemToWidget(pdf_path, 'pdf_path')
        }
        //Load Settings
        window.Alteryx.Gui.AfterLoad = function (manager) {
          //Set WorkflowDirectory
          this.rotate_angle = manager.getDataItem("rotate_angle").getValue()
          this.pdf_page = manager.getDataItem("pdf_page").getValue()
          //Load Income Field
          // let str_type = ["String", "WString", "V_String", "V_WString", "Date", "Time", "DateTime"]
          // let val_type = ["Byte", "Int16", "Int32", "Int64", "FixedDecimal", "Float", "Double"]
          // let incomingFields = manager.getIncomingFields()
          // this.str_columns = incomingFields.filter(item => str_type.indexOf(item.strType) > -1).map(item => item.strName)
          // this.val_columns = incomingFields.filter(item => val_type.indexOf(item.strType) > -1).map(item => item.strName)
        }.bind(this)
      }.bind(this)
      //Load Script
      document.head.appendChild(script)
    }
  },
  computed: {
    // legder_status: function () {
    //   try {
    //     //是否連接資料
    //     if ((this.str_columns.length + this.val_columns.length) === 0) {
    //       throw `未連接pdf檔案 !`
    //     }
    //     return true
    //   } catch (err) {
    //     return err
    //   }
    // },
  },
  methods: {
  }
}
</script>

<style>
#app {
  font-family: "Helvetica Neue", Helvetica, Arial, "Microsoft JhengHei", "PingFang TC", "Heiti TC", sans-serif;
  display: flex;
  flex-direction: column;
  height: 100%;
}

html,
body {
  height: 100%;
}
</style>
