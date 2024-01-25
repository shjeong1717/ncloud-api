# Get monitor group
def getMonitorGrpKey(param):
  result = monitor.send_api(param)
  listData = json.loads(result)['data']
  print("================= Monitor Group Key =================")
  for data in listData:
    print(data['groupName'] +" : "+ data['id'])
  #end for
#end def

# Get metric group
def getMetricGrpKey(param):
  result = metric.send_api(param)
  listData = json.loads(result)
  print("================= Metric Group Key =================")
  for data in listData:
    print(data['groupName'] +" : "+ data['id'])
  #end for
#end def

# Get noti info
def getNotiInfo():
  result = noti.send_api()
  rsltData = json.loads(result)['data']
  print("================= Notification Info =================")
  for data in rsltData:
    print(data)
  # end for
#end def

# Get system schema list
def getSystemSchemaList():
  result = schema.send_api()
  rsltData = json.loads(result)
  print("================= System Schema Info =================")
  objList = []
  for data in rsltData['data']:
    objData = {}
    objData[data['prodName']] = data['cw_key']
    objList.append(objData)
    print(data["prodName"] +" : "+ data["cw_key"])
  # end for
# end def

# Get rule group list
def getRuleGroupIdList(param):
  result = rule.send_api(param)
  rsltData = json.loads(result)
  print("================= Rule Group Info =================")
  finData = []
  for data in rsltData['data']['ruleGroups']:
    objData = {}
    objData['prodKey'] = data['prodKey']
    objData['groupName'] = data['groupName']
    objData['ruleGroupId'] = data['id']
    finData.append(objData)
  # end for
  print(json.dumps(finData, indent=2))
# end def

# Get rule group list
def getRuleGroupList(param):
  result = rule.send_api(param)
  rsltData = json.loads(result)
  print("================= Rule Group Info =================")
  finData = []
  for data in rsltData['data']['ruleGroups']:
    objData = {}
    objData['prodKey'] = data['prodKey']
    objData['groupName'] = data['groupName']
    objData['ruleGroupId'] = data['id']
    
    objData['monitorGroups'] = []
    for monitor in data['monitorGroups']:
      objMonitor = {}
      objMonitor['id'] = monitor['id']
      objMonitor['monitorGroupItemList'] = monitor['monitorGroupItemList']
      if 'groupName' in monitor:
        objMonitor['groupName'] = monitor['groupName']
      if 'groupDesc' in monitor:
        objMonitor['groupDesc'] = monitor['groupDesc']
      #end if
      objData['monitorGroups'].append(objMonitor)
    #end for
    
    objData['metricsGroups'] = []
    for metric in data['metricsGroups']:
      objMetric = {}
      objMetric['id'] = metric['id']
      if 'groupName' in metric:
        objMetric['groupName'] = metric['groupName']
      # end if
      if 'groupDesc' in metric:
        objMetric['groupDesc'] = metric['groupDesc']
      #end if
      
      objMetric['metrics'] = []
      for metricItem in metric['metrics']:
        objItem = {}
        objItem['metric'] = metricItem['metric']
        objItem['metricGroupItemId'] = metricItem['metricGroupItemId']
        objMetric['metrics'].append(objItem)
      #end for
      objData['metricsGroups'].append(objMetric)
    #end for
    finData.append(objData)
  # end for
  print(json.dumps(finData, indent=2))
# end def