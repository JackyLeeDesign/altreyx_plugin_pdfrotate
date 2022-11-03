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
          <div class="card-header d-flex justify-content-between align-items-center"><b>Step1：請選擇 PDF 檔案：</b></div>
          <div class="card-body" style="overflow-x:auto;">
            <label for="exampleFormControlInput1" class="form-label"><b>
                <BIconFiles style="vertical-align:text-top;" class="icon" />本元件將所選之 PDF 檔進行特定角度的翻轉。
              </b></label>
            <button type="button" class="btn" style="padding:0px;" v-on:click="help_1 = !help_1">
              <span v-if="!help_1"><BIconEyeFill style="vertical-align:text-top;" class="icon" /> 檢視教學</span>
              <span v-if="help_1"><BIconEyeSlashFill style="vertical-align:text-top;" class="icon" /> 隱藏教學</span>
            </button>
            <br>
              <div v-if="help_1">
                <div class="mb-3" style="display:grid;justify-content:space-around;">
                  <label class="form-label"><b>1.可於元件前連結其他元件或直接選擇 PDF 檔案，若您是直接選擇 PDF 檔案則可跳過 2~3 步驟。</b></label>
                  <img src="./step_1_1.png" style="width: 100%;max-width:650px;">
                </div>
                <div class="mb-3" style="display:grid;justify-content:space-around;">
                  <label class="form-label"><b>2.連結輸入資料後，因資料可能包含多個欄位，確認"檔案路徑"欄位。(下圖以資料夾工具為範例，其輸出結果有許多欄位，但只有路徑欄位才是我們需要的，故此處我們選擇 fullpath 完整路徑欄位，提供後續轉置元件處理)</b></label>
                  <img src="./step_1_2.png" style="width: 100%;max-width:650px;">
                </div>
                <div class="mb-3" style="display:grid;justify-content:space-around;">
                  <label class="form-label"><b>3.選擇欄位。</b></label>
                  <img src="./step_1_3.png" style="width: 100%;max-width:650px;">
                </div>
                <div class="mb-3" style="display:grid;justify-content:space-around;">
                  <label class="form-label"><b>若前面接的是 PDF 合併元件，按同樣邏輯，我們選擇路徑欄位 Output Path 即可。</b></label>
                  <img src="./step_1_4.png" style="width: 100%;max-width:650px;">
                </div>
              </div>
            <ayx v-if="input_isConnectFile !== true" data-ui-props='{type:"FileBrowse", widgetId:"pdf_path", browseType:"File", fileTypeFilters: "PDF Files (*.pdf)|*.pdf"}'></ayx>
            <div class="mb-3">
              <label v-if="input_isConnectFile === true" for="exampleFormControlInput1" class="form-label"><b>
                  <BIconColumns style="vertical-align:text-top;" class="icon" />根據您所連接的檔案，請選擇其輸出路徑 (Output) 欄位
                </b></label>
                <select v-if="input_isConnectFile === true" class="form-control" v-model="connectInputPathMapping">
                  <option disabled value="">選擇欄位</option>
                  <option v-for="item,index in str_columns" v-bind:key="index">{{item}}</option>
                </select>
            </div>
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
          <div class="card-header d-flex justify-content-between align-items-center"><b>Step3：請選擇待處理頁數</b></div>
          <div class="card-body" style="overflow-x:auto;">
            <div class="form-check mb-3">
              <input type="checkbox" class="form-check-input" v-model="pdf_isToDoAll" />
              <label for="exampleFormControlInput1" class="form-check-label"><b>
                  處理所有頁數
                </b></label>
            </div>
            <div class="mb-3" v-if="pdf_isToDoAll === false">
              <label for="exampleFormControlInput1" class="form-label"><b>
                  <BIconColumns style="vertical-align:text-top;" class="icon" /> 跨頁數請用","分隔，如:1,3,5。 某範圍頁數可用 "-"
                  表示，如:1-3。
                  亦可搭配使用，如:1-3,5,7
                </b></label>
              <input type="text" id="exampleFormControlInput1" class="form-control" placeholder="輸入頁數"
                v-model="pdf_page">
            </div>
          </div>
        </div>

      </div>
    </div>
  </div>

  <footer class="footer mt-auto">
    <p class="text-muted" style="margin: 0px;text-align: center;">版本：0.2.5</p>
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
      pdf_isToDoAll: true,
      connectInputPathMapping:"",
      input_isConnectFile:false,
      help_1:false,
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
    input_isConnectFile:{
      handler(val) {
        if (typeof window.Alteryx !== 'undefined') {
          window.Alteryx.Gui.Manager.getDataItem("input_isConnectFile").setValue(val)
        }
      },
      deep: true
    },
    connectInputPathMapping:{
      handler(val) {
        if (typeof window.Alteryx !== 'undefined') {
          window.Alteryx.Gui.Manager.getDataItem("connectInputPathMapping").setValue(val)
        }
      },
      deep: true
    },
    rotate_angle: {
      handler(val) {
        if (typeof window.Alteryx !== 'undefined') {
          window.Alteryx.Gui.Manager.getDataItem("rotate_angle").setValue(val)
        }
      },
      deep: true
    },
    pdf_page: {
      handler(newVal, oldVal) {
        if (!newVal) {
          return
        }
        let inputStr = newVal.replaceAll(" ", "")
        let pageArray = inputStr.split(',')

        // 頁數檢查
        pageArray.map(page => {
          //判斷是否為數字或"-"
          if (isNaN(page.replaceAll("-", "")) == true || page.includes('.')) {
            console.log(page)
            alert("頁數必須為數字")
            this.pdf_page = oldVal
            return;
          }
          if (page.includes('-')) {
            //判斷是否輸入多個'-'
            let count = (page.match(/-/g)).length;
            if (count > 1) {
              alert("不可輸入多個'-'字元")
              this.pdf_page = oldVal
              return;
            }
          }
        })

        if (typeof window.Alteryx !== 'undefined') {
          window.Alteryx.Gui.Manager.getDataItem("pdf_page").setValue(newVal)
        }
      },
      deep: true
    },
    pdf_isToDoAll: {
      handler(val) {
        if (typeof window.Alteryx !== 'undefined') {
          window.Alteryx.Gui.Manager.getDataItem("pdf_isToDoAll").setValue(val)
        }
      },
      deep: true
    }
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
          var pdf_isToDoAll = new AlteryxDataItems.SimpleBool('pdf_isToDoAll')
          manager.addDataItem(pdf_isToDoAll)
          var connectInputPathMapping = new AlteryxDataItems.SimpleString('connectInputPathMapping')
          manager.addDataItem(connectInputPathMapping)
          var input_isConnectFile = new AlteryxDataItems.SimpleBool('input_isConnectFile')
          manager.addDataItem(input_isConnectFile)
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
          this.pdf_isToDoAll = manager.getDataItem("pdf_isToDoAll").getValue()
          this.connectInputPathMapping = manager.getDataItem("connectInputPathMapping").getValue()
          this.input_isConnectFile = manager.getDataItem("input_isConnectFile").getValue()
          
          // Load Income Field
          let str_type = ["String", "WString", "V_String", "V_WString", "Date", "Time", "DateTime"]
          let val_type = ["Byte", "Int16", "Int32", "Int64", "FixedDecimal", "Float", "Double"]
          let incomingFields = manager.getIncomingFields()
          this.str_columns = incomingFields.filter(item => str_type.indexOf(item.strType) > -1).map(item => item.strName)
          this.val_columns = incomingFields.filter(item => val_type.indexOf(item.strType) > -1).map(item => item.strName)
          
          if ((this.str_columns.length + this.val_columns.length) === 0) {
            this.input_isConnectFile = false;
          }
          else{
            this.input_isConnectFile = true;
          }
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
    //       throw `連結的檔案欄位為空 !`
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
