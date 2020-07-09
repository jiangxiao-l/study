

function initTable(tableid, coldata, url){
            $.fn.editable.defaults.mode = 'inline';
            $('#'+tableid).bootstrapTable({
                url: url,         //请求后台的URL（*）
                method: 'get',                      //请求方式（*）
                toolbar: '#toolbar',                //工具按钮用哪个容器
                striped: true,                      //是否显示行间隔色
                cache: false,                       //是否使用缓存，默认为true，所以一般情况下需要设置一下这个属性（*）
                pagination: true,                   //是否显示分页（*）
                sortable: false,                     //是否启用排序
                sortOrder: "asc",                   //排序方式
                sidePagination: "client",           //分页方式：client客户端分页，server服务端分页（*）
                pageNumber:1,                       //初始化加载第一页，默认第一页
                pageSize: 10,                       //每页的记录行数（*）
                pageList: [10, 25, 50, 100],        //可供选择的每页的行数（*）
                //search: true,                       //是否显示表格搜索，此搜索是客户端搜索，不会进服务端，所以，个人感觉意义不大
                strictSearch: true,
                showPaginationSwitch: true,
                showColumns: true,                  //是否显示所有的列
                showRefresh: true,                  //是否显示刷新按钮
                clickToSelect: true,                //是否启用点击选中行
                uniqueId: "id",                     //每一行的唯一标识，一般为主键列
                showToggle:true,                    //是否显示详细视图和列表视图的切换按钮
                cardView: false,                    //是否显示详细视图
                detailView: false,                   //是否显示父子表
                showExport: true,                     //是否显示导出
                exportDataType: "basic",              //basic', 'all', 'selected'.


                onEditableSave: function (field, row, oldValue, $el) {
                    // delete row[0];
                    updata = {};
                    updata[field] = row[field];
                    updata['id'] = row['id'];
                    $.ajax({
                        type: "POST",
                        url: "/backend/modify/",
                        data: { postdata: JSON.stringify(updata), 'action':'edit' },
                        success: function (data, status) {
                            if (status == "success") {
                                alert("编辑成功");
                            }
                        },
                        error: function () {
                            alert("Error");
                        },
                        complete: function () {

                        }
                    });
                },
                columns: coldata
            });
        }


function deleteData(tableid) {
            //获取所有被选中的记录
            var rows = $("#"+tableid).bootstrapTable('getSelections');
            if (rows.length== 0) {
                alert("请先选择要删除的记录!");
                return;
            }
            var ids = [];
            for (var i = 0; i < rows.length; i++) {
                ids.push(rows[i]['id']);
            }

            var msg = "您真的确定要删除吗？";
            if (confirm(msg) == true) {
                $.ajax({
                    url: "/backend/modify/",
                    type: "post",
                    traditional: true,
                    data: {'ids': ids, 'action':'del'},
                    success: function (data) {
                        alert(data);
                        //重新加载数据
                        $("#servers").bootstrapTable('refresh');
                    }
                });
            }
        }