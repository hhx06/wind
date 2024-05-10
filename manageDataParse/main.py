#!/usr/bin/env python
# -*- coding:utf-8
"""
@FileName :main.py
@Time :2024/4/817:24
@Author :Hhx06
@Desc : 打点数据解析
"""
import csv
import re


# 字符串是否含有某字符
def contains_char(s, char):
    return char in s


def contains_char_not(s, char):
    return char not in s


# 打开CSV文件
def readCsv(filePath):
    with open(filePath, 'r', encoding='utf-8') as csvfile:
        reader = filePath.reader(csvfile)
        # 遍历每一行数据
        for row in reader:
            # 处理每一行数据
            print(row)
            print("==============")


def readTxt(filePath, myMap, myTps):
    x = False
    with open(filePath, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        for line in lines:
            # print(line.strip())
            if contains_char(line.strip(), "CostTime") and contains_char_not(line.strip(), "总体最热"):
                x = False
            if contains_char(line.strip(), "总体最热"):
                x = True
                result = line.strip().split(" ")
                if len(result) > 0:
                    k = 0
                    for v in result:
                        k += 1
                        if contains_char(v, "userCount"):
                            break
                    if k > 0 and len(result) > k + 1:
                        userCount = result[k]
                    # print("userCount:", userCount)
            if x:
                if contains_char(line.strip(), "hot"):
                    if userCount == 0:
                        continue
                    # 多个空格合为一个空格
                    result = re.sub(r'\s+', " ", line.strip()).split(" ")
                    # print("before")
                    for v in range(0, len(result)):
                        if result[v] == "hot" and len(result) > v + 5 and contains_char(result[v + 1], "ms"):
                            respTimeAll = result[v + 1][:-2]
                            messageCount = result[v + 4]
                            messageName = result[v + 5]
                            avgTime = float(respTimeAll) / float(messageCount)
                            if messageName not in myMap:
                                myMap[messageName] = [avgTime]
                            else:
                                myMap[messageName].append(avgTime)
                            maxTps = float(messageCount) / float(userCount) / float(60)
                            if myTps.get(messageName, {"tps": float('-inf')})["tps"] < maxTps:
                                myTps[messageName] = {"messageName": messageName, "tps": maxTps}
    return myMap, myTps


def getSortData(myMap, myTps, t):
    sum100 = 0
    for k, v in myMap.items():
        if len(v) >= 10:
            # 不会产生新的dist
            v.sort()
            v = v[:int(len(v) * 9 / 10)]
        myTps[k]["respTime"] = sum(v) / len(v)
        myTps[k]["costTps"] = sum(v) / len(v) * myTps[k]["tps"]
        t[k] = myTps[k]
        sum100 += myTps[k]["costTps"]
    return sorted(t.items(), key=lambda x: x[1]['costTps']), sum100


def main():
    myMap = {}
    myTps = {}
    t = {}
    # myMap, myTps = readTxt("./proto_stat.log", myMap, myTps)
    myMap, myTps = readTxt("./output.txt", myMap, myTps)
    # print("myMap:", myMap)
    # print("myTps:", myTps)
    tt, sum100 = getSortData(myMap, myTps, t)
    writeCsv("./90.csv", tt, sum100)
    # writeCsv("./x.csv", tt, sum100)


def writeCsv(new_csv, tt, sum100):
    sum90 = 0
    with open(new_csv, 'w+', newline='', encoding='gb18030') as csvfile:
        spamWriter = csv.writer(csvfile, dialect="excel")  # dialect可用delimiter= ','代替，后面的值是自己想要的符号
        # 如：spamWriter = csv.writer(csvfile,delimiter= '：')#dialect可用delimiter= ','
        spamWriter.writerow(
            ["协议", "最大人均tps", "单协议平均耗时", "单协议耗时*人均最大TPS", "是否压测", "协议名称"])
        data = dataX()
        for k, val in tt:
            w = ""
            sum90 += val["costTps"]
            line_data = []
            print(val)
            for k1, v1 in val.items():
                print(v1)
                line_data.append(v1)
            if sum90 > sum100 * 0.90:
                line_data.append("否")
            else:
                line_data.append("是")
            if line_data[0] in data:
                w = data[line_data[0]]
            line_data.append(w)
            spamWriter.writerow(line_data)


def dataX():
    data = {}

    # 数据
    data_str = """
            MSG_ENUM_DEFAULT = 0;

      MSG_BEGIN = 100000;//cs协议开始
      MSG_END = 199999;//cs协议结束

      MSG_C2S_Flush = 100001;//flush协议 刷新基础数据
      MSG_S2C_Flush = 100002;//返回原则：有定量的可以合并到该协议 会自增长的单独协议
      MSG_S2C_OpObject = 100003;//身上状态变更
      MSG_C2S_SyncTime = 100004;//同步时间信息
      MSG_S2C_SyncTime = 100005;
      MSG_C2S_SyncProto = 100006; //同步响应缓存
      MSG_S2C_SyncProto = 100007;
      MSG_S2C_GetAwardNotify = 100008; //掉落推送
      MSG_S2C_FlushUser = 100009; //输出玩家
      MSG_S2C_FlushResource = 100010; //输出资源
      MSG_S2C_FlushItem = 100011; //输出道具
      MSG_S2C_FlushRedPoint = 100012; //输出红点
      MSG_S2C_FlushServerInfo = 100013; //服务器信息
      MSG_S2C_FlushToken = 100014; //推送凭证
      MSG_C2S_GM_Cmd = 100015; //GM指令
      MSG_S2C_GM_Cmd = 100016; //GM指令
      MSG_S2C_FlushCharacter = 100017; //推送角色
      MSG_S2C_FlushFormation = 100018; //推送阵容
      MSG_S2C_FlushEquip = 100019; //输出装备
      MSG_S2C_FlushTreasureBox = 100020; //输出宝箱数据
      MSG_S2C_FlushMainDungeon = 100021; //输出主线副本
      MSG_S2C_FlushHangUp = 100022; //输出挂机数据
      MSG_S2C_FlushUserGuide = 100024;  //输出玩家引导数据
      MSG_S2C_FlushUserWorldBoss = 100025; //输出世界Boss 信息
      MSG_S2C_FlushUserPlayNum = 100026; //输出玩法数据信息
      MSG_S2C_FlushUserShare = 100027; //输出分享数据
      MSG_S2C_FlushUserArena = 100028; //输出玩家竞技场数据
      MSG_S2C_FlushScoreShop = 100029; //输出积分商店
      MSG_S2C_FlushFragment = 100030; //输出碎片
      MSG_S2C_FlushRecruit = 100031; //输出卡池
      MSG_S2C_FlushRecharge = 100033; //输出充值
      MSG_S2C_FlushInfiniteDungeon = 100034; //输出地牢
      MSG_S2C_FlushUserFriendSystem = 100035; //输出好友系统
      MSG_S2C_FlushUserChat = 100036; //输出聊天
      MSG_S2C_FlushUserArtifact = 100037; //推送神器
      MSG_S2C_FlushUserGuildBoss = 100038; //输出公会BOSS
      MSG_S2C_FlushUserGuild = 100039; //输出公会
      MSG_S2C_FlushBattlePass = 100040; //输出战令
      MSG_S2C_FlushUserCasualGame = 100041; //输出小游戏
      MSG_S2C_FlushUserMow = 100042; //输出割草
      MSG_S2C_FlushDailySpecials = 100043; //输出每日特惠
      MSG_S2C_FlushUserFund = 100044; //输出基金
      MSG_S2C_FlushActivityOpen = 100045; //输出开服活动
      MSG_S2C_FlushFirstRecharge = 100046; //输出首充
      MSG_S2C_FlushAccumulatedRecharge = 100047; //输出累充
      MSG_S2C_FlushMonthlyCard = 100048; //输出月卡
      MSG_S2C_FlushAvatar = 100049; //输出头像&头像框
      MSG_S2C_FlushUserDailySign = 100050; //输出每日签到
      MSG_S2C_FlushUserPushGift = 100052; //输出推送礼包
      MSG_S2C_FlushUserSevenSign = 100053; //输出七日签到
      MSG_S2C_FlushSevenAct = 100054; //输出七日活动
      MSG_S2C_FlushAchievement = 100056; //输出成就
      MSG_S2C_FlushUserPrivilege = 100057; // 输出特权
      MSG_S2C_FlushBack = 100058; // 输出背饰背包
      MSG_S2C_FlushUserBack = 100059; // 输出背饰
      MSG_S2C_FlushUserTower = 100060; // 输出爬塔数据
      MSG_S2C_FlushCompanionBook = 100061; // 输出佣兵图鉴
      MSG_S2C_FlushHonor = 100062; // 输出头衔
      MSG_S2C_FlushUserSeriesGift = 100063;  // 输出一条龙礼包
      MSG_S2C_FlushUserDailySurpriseBenefit = 100064;  // 输出每日惊喜福利
      MSG_S2C_FlushUserFunctionPreview = 100065;  // 输出功能预览
      MSG_S2C_FlushDress = 100066; // 输出时装
      MSG_S2C_FlushUserTreasury = 100067;  // 输出宝库
      MSG_S2C_FlushAdvertise = 100068; // 输出广告数据
      MSG_S2C_FlushQuestionnaire = 100069; // 输出问卷

      MSG_C2S_Test_OpManager = 100090; //OP操作
      MSG_S2C_Test_OpManager = 100091; //OP操作响应
      MSG_C2S_Test_PVEBattleBegin = 100092;//测试异步战斗(PVE)
      MSG_S2C_Test_PVEBattleBegin = 100093;
      MSG_S2C_Test_PVEBattleFinish = 100094;
      MSG_C2S_Test_PVPBattleBegin = 100095;//测试异步战斗(PVP)
      MSG_S2C_Test_PVPBattleBegin = 100096;
      MSG_S2C_Test_PVPBattleFinish = 100097;

      MSG_C2S_CommonRank_GetList = 100115;//获取通用排行榜信息
      MSG_S2C_CommonRank_GetList = 100116;
      MSG_C2S_FirstRecord_GetInfo = 100117; // 获取首通记录
      MSG_S2C_FirstRecord_GetInfo = 100118;

      MSG_S2C_User_NotifyKickOut = 100120; //踢线消息
      MSG_C2S_UserInfo_ModifyName = 100121; //修改昵称
      MSG_S2C_UserInfo_ModifyName = 100122; //修改昵称响应
      MSG_C2S_UserInfo_GetDetail = 100123;  // 获取玩家详细信息
      MSG_S2C_UserInfo_GetDetail = 100124;

      MSG_C2S_Item_Use = 100250; //使用道具
      MSG_S2C_Item_Use = 100251; //使用道具响应
      MSG_C2S_Diamond_Exchange = 100252; //付费钻石兑换绑钻
      MSG_S2C_Diamond_Exchange = 100253;

      //API account(100951-100960)
      MSG_S2C_API_GetRoleList = 100951; //获取角色信息
      MSG_S2C_API_SearchUser = 100952; //搜索用户

      // 通用打开数据埋点协议(100961-100970)
      MSG_C2S_Log_OpenPanel = 100961; //客户端打开面板触发日志埋点
      MSG_S2C_Log_OpenPanel = 100962;

      // 0.1.0-开宝箱协议(101000-101035)
      // TODO: 公会目前没有该系统暂时不定义，等以后有了再补充
      MSG_C2S_TreasureBox_Open = 101000;                  // 手动开宝箱
      MSG_S2C_TreasureBox_Open = 101001;
      MSG_C2S_TreasureBox_SetAutoOpenCondition = 101004;  // 设置自动开启的条件
      MSG_S2C_TreasureBox_SetAutoOpenCondition = 101005;
      MSG_C2S_TreasureBox_Upgrade = 101006;               // 宝箱升级
      MSG_S2C_TreasureBox_Upgrade = 101007;
      MSG_C2S_TreasureBox_ItemUpSpeedTime = 101008;       // 道具加速升级时间
      MSG_S2C_TreasureBox_ItemUpSpeedTime = 101009;
      MSG_C2S_TreasureBox_AdvertiseUpSpeedTime = 101010;  // 道具加速升级时间
      MSG_S2C_TreasureBox_AdvertiseUpSpeedTime = 101011;
      MSG_C2S_TreasureBox_AutoOpen = 101016;              // 自动开宝箱
      MSG_S2C_TreasureBox_AutoOpen = 101017;
      MSG_C2S_TreasureBox_BuyUpgradeCnt = 101018;         // 购买消耗道具,本质上升级小段
      MSG_S2C_TreasureBox_BuyUpgradeCnt = 101019;
      MSG_C2S_TreasureBox_ChestUpgradeFinish = 101020;    // 没有啥用标记用
      MSG_S2C_TreasureBox_ChestUpgradeFinish = 101021;

      // 0.1.0-挂机奖励领取(101036-101039)
      MSG_C2S_HangUp_ObtainAwards = 101036;               // 领取挂机奖励
      MSG_S2C_HangUp_ObtainAwards = 101037;
      MSG_C2S_HangUp_UseItemObtainAwards = 101038;        // 使用道具获取挂机奖励
      MSG_S2C_HangUp_UseItemObtainAwards = 101039;


      //0.1.0-主线任务(101040-101060)
      MSG_S2C_QuestMain_Flush = 101041; //主线任务信息推送
      MSG_C2S_QuestMain_GetReward = 101042; //领取主线任务奖励
      MSG_S2C_QuestMain_GetReward = 101043; //领取主线任务奖励响应

      // 0.1.0-主线副本(101080-101100)
      MSG_C2S_MainDungeon_ChallengeBegin = 101080;         // 主线副本-发起挑战
      MSG_S2C_MainDungeon_ChallengeBegin = 101081;
      MSG_S2C_MainDungeon_ChallengeFinish = 101082;        // 主线副本-结束挑战
      MSG_C2S_MainDungeon_ObtainAward = 101084;            // 主线副本-领取关卡奖励
      MSG_S2C_MainDungeon_ObtainAward = 101085;
      MSG_C2S_MainDungeon_GetStageRecordInfo = 101086;     // 主线副本-获取关卡的战斗记录
      MSG_S2C_MainDungeon_GetStageRecordInfo = 101087;
      MSG_C2S_MainDungeon_OnekeyObtainChapterStageRewards = 101088;     // 主线副本-一键领取章节阶段奖励
      MSG_S2C_MainDungeon_OnekeyObtainChapterStageRewards = 101089;
      MSG_C2S_MainDungeon_ObtainChapterRewards = 101090;           // 主线副本领取章节奖励
      MSG_S2C_MainDungeon_ObtainChapterRewards = 101091;


      // 0.1.0-装备系统(101101-101110)
      MSG_C2S_Equipment_Wear = 101101;             // 穿戴装备
      MSG_S2C_Equipment_Wear = 101102;
      MSG_C2S_Equipment_Sale = 101103;             // 出售装备
      MSG_S2C_Equipment_Sale = 101104;
      MSG_C2S_Equipment_Illusion = 101105;         // 装备幻化
      MSG_S2C_Equipment_Illusion = 101106;

      //0.2.0-邮件系统(101111-101130)
      MSG_C2S_Mail_Info = 101111;  // 获取邮件
      MSG_S2C_Mail_Info = 101112;
      MSG_C2S_Mail_Award = 101113;  // 领取邮件奖励
      MSG_S2C_Mail_Award = 101114;
      MSG_C2S_Mail_Del = 101115;  // 删除邮件
      MSG_S2C_Mail_Del = 101116;
      MSG_C2S_Mail_Read = 101117;  // 阅读邮件
      MSG_S2C_Mail_Read = 101118;
      MSG_S2C_Mail_New = 101119; // 新邮件推送

      //0.1.0-主角养成(101161-101200)
      //0.1.0-技能树
      MSG_C2S_SkillTree_Upgrade = 101161; //主角技能树升级
      MSG_S2C_SkillTree_Upgrade = 101162; //主角技能树升级响应
      //0.2.0-主角转职
      MSG_C2S_MainCharacter_Switch = 101163; //主角转职
      MSG_S2C_MainCharacter_Switch = 101164; //主角转职响应

      //0.1.0-玩家引导数据(101250-101300)
      MSG_C2S_Guide_BattleRecord = 101250;   // 新手引导战斗记录
      MSG_S2C_Guide_BattleRecord = 101251;
      MSG_C2S_Guide_SaveRecord = 101252;      // 新手引导各种类型计数
      MSG_S2C_Guide_SaveRecord = 101253;

      //0.1.0-世界Boss(101301-101320)
      MSG_C2S_WorldBoss_RespawnBoss = 101301;       // 复活 Boss
      MSG_S2C_WorldBoss_RespawnBoss = 101302;
      MSG_C2S_WorldBoss_ChallengeBegin = 101303;   // 开始挑战 Boss
      MSG_S2C_WorldBoss_ChallengeBegin = 101304;
      MSG_S2C_WorldBoss_ChallengeFinish = 101305;  // 挑战Boss 结束

      //0.1.0-玩法次数(101321-101340)
      MSG_C2S_PlayNum_BuyCnt = 101321;     // 购买玩法次数
      MSG_S2C_PlayNum_BuyCnt = 101322;     // 购买玩法次数

      //0.2.0-阵位信息(101351-101370)
      MSG_C2S_Formation_Upgrade = 101351;  // 升级阵位
      MSG_S2C_Formation_Upgrade = 101352;
      MSG_C2S_Formation_Exchange = 101353;  // 交换位置(上下阵)
      MSG_S2C_Formation_Exchange = 101354;
      MSG_C2S_Formation_ExchangeBattle = 101355;      // 交换布阵位置
      MSG_S2C_Formation_ExchangeBattle = 101356;
      MSG_C2S_Formation_SaveBattleTeam = 101357;      // 保存当前布阵阵容
      MSG_S2C_Formation_SaveBattleTeam = 101358;
      MSG_C2S_Formation_RecoveryBattleTeam = 101359;  // 恢复指定的阵容作为当前阵容
      MSG_S2C_Formation_RecoveryBattleTeam = 101360;
      MSG_C2S_Formation_RenameBattleTeam = 101361;    // 队伍修改名字
      MSG_S2C_Formation_RenameBattleTeam = 101362;
      MSG_C2S_Formation_Get = 101363;    // 获取指定阵容
      MSG_S2C_Formation_Get = 101364;

      //0.2.0-佣兵养成(101400-101450)
      MSG_C2S_CharacterCompanion_UpgradeQuality = 101400;  // 佣兵升级品质(佣兵升星)
      MSG_S2C_CharacterCompanion_UpgradeQuality = 101401;

      //0.2.0-竞技场(101500-101530)
      MSG_C2S_Arena_MatchOpponent = 101500;    // 竞技场匹配(手动刷新)
      MSG_S2C_Arena_MatchOpponent = 101501;
      MSG_C2S_Arena_Like = 101502;             // 竞技场点赞
      MSG_S2C_Arena_Like = 101503;
      MSG_C2S_Arena_Enter = 101504;            // 进入玩法
      MSG_S2C_Arena_Enter = 101505;
      MSG_C2S_Arena_ChallengeBegin = 101510;   // 竞技场挑战开始
      MSG_S2C_Arena_ChallengeBegin = 101511;
      MSG_S2C_Arena_ChallengeFinish = 101512;  // 竞技场挑战结束
      MSG_C2S_Arena_GetScoreRank = 101513;     // 竞技场获取积分榜单数据
      MSG_S2C_Arena_GetScoreRank = 101514;
      MSG_C2S_Arena_GetBattleRecord = 101515;  // 获取对战记录
      MSG_S2C_Arena_GetBattleRecord = 101516;
      MSG_C2S_Arena_GetTaskAward = 101517;     // 获取竞技场任务奖励
      MSG_S2C_Arena_GetTaskAward = 101518;
      MSG_C2S_Arena_OneKeyGetTaskAward = 101519; // 一键领取每日任务奖励
      MSG_S2C_Arena_OneKeyGetTaskAward = 101520; // 一键领取每日任务奖励
      MSG_C2S_Arena_SetDefendFormation = 101521; // 设置防守阵容
      MSG_S2C_Arena_SetDefendFormation = 101522;
      MSG_S2C_Arena_NotifyAttacked = 101523;     // 竞技场通知被打

      //0.2.0-积分商店(101531-101540)
      MSG_C2S_ScoreShop_Buy = 101531;    // 积分商店购买
      MSG_S2C_ScoreShop_Buy = 101532;
      MSG_C2S_ScoreShop_GetRefreshShop = 101533; // 获取刷新商店格子列表
      MSG_S2C_ScoreShop_GetRefreshShop = 101534;

      // 0.1.5-分享(101541-101560)
      MSG_C2S_Share_Award = 101541;        // 分享获得奖励
      MSG_S2C_Share_Award = 101542;

      //0.2.0-佣兵抽卡(101561-101580)
      MSG_C2S_Recruit_Roll = 101561; //抽卡
      MSG_S2C_Recruit_Roll = 101562;
      MSG_C2S_Recruit_AwardExtra = 101563; //领取额外奖励
      MSG_S2C_Recruit_AwardExtra = 101564;

      // 0.2.0-碎片(101581-101600)
      MSG_C2S_Fragment_Compose = 101581; //碎片合成
      MSG_S2C_Fragment_Compose = 101582;

      //0.2.0-行为类计数(101601-101602)
      MSG_C2S_FlushQuest = 101601; //刷新行为类计数
      MSG_S2C_FlushQuest = 101602;

      //0.3.0-地牢(101651-101670)
      MSG_C2S_InfiniteDungeon_ChallengeBegin = 101651; // 地牢-发起挑战
      MSG_S2C_InfiniteDungeon_ChallengeBegin = 101652;
      MSG_S2C_InfiniteDungeon_ChallengeFinish = 101653; // 地牢-结束挑战
      MSG_C2S_InfiniteDungeon_GetStageRecordInfo = 101656; // 地牢-获取关卡的战斗记录
      MSG_S2C_InfiniteDungeon_GetStageRecordInfo = 101657;
      MSG_C2S_InfiniteDungeon_AwardHangup = 101658; // 地牢-领取挂机奖励
      MSG_S2C_InfiniteDungeon_AwardHangup = 101659;
      MSG_C2S_InfiniteDungeon_StartHangup = 101660; // 首次进入地牢界面开始挂机
      MSG_S2C_InfiniteDungeon_StartHangup = 101661;
      // 0.3.0-好友系统(101701-101750)
      MSG_C2S_Friend_Apply = 101701;           // 好友申请
      MSG_S2C_Friend_Apply = 101702;
      MSG_C2S_Friend_Ack = 101703;             // 好友应答
      MSG_S2C_Friend_Ack = 101704;
      MSG_C2S_Friend_Search = 101705;          // 好友搜索
      MSG_S2C_Friend_Search = 101706;
      MSG_C2S_Friend_Recommend = 101707;       // 好友推荐
      MSG_S2C_Friend_Recommend = 101708;
      MSG_C2S_Friend_DelFriend = 101709;       // 删除好友
      MSG_S2C_Friend_DelFriend = 101710;
      MSG_C2S_Friend_AddBlack = 101711;        // 添加黑名单
      MSG_S2C_Friend_AddBlack = 101712;
      MSG_C2S_Friend_DelBlack = 101713;        // 删除黑名单
      MSG_S2C_Friend_DelBlack = 101714;
      MSG_C2S_Friend_GiveGift = 101715;        // 送好友礼物
      MSG_S2C_Friend_GiveGift = 101716;
      MSG_C2S_Friend_AcceptGift = 101717;      // 接收好友礼物
      MSG_S2C_Friend_AcceptGift = 101718;
      MSG_S2C_Friend_NotifyApply = 101719;     // 通知申请好友
      MSG_S2C_Friend_NotifyAck = 101720;       // 通知好友
      MSG_S2C_Friend_NotifyDelFriend = 101721; // 通知删除好友
      MSG_S2C_Friend_NotifyGiveGift = 101722;  // 通知赠送礼物
      MSG_S2C_Friend_NotifyAddBlack = 101723;  // 通知拉黑名单
      // 0.3.0-聊天(101751-101780)
      MSG_C2S_Chat_Content = 101751;          // 聊天
      MSG_S2C_Chat_Content = 101752;
      MSG_S2C_Chat_Notify_Content = 101753;   // 通知聊天消息
      MSG_S2C_Chat_Notify_System = 101754;    // 通知系统消息
      MSG_S2C_Chat_SetForbidPrivate = 101755; // 设置禁止私聊
      MSG_C2S_Chat_SetForbidPrivate = 101756; // 设置禁止私聊
      MSG_C2S_Chat_GetForbidPrivate = 101757; // 获取玩家是否设置禁止私聊
      MSG_S2C_Chat_GetForbidPrivate = 101758;
      MSG_S2C_Chat_Notify_GuildSystem = 101759; // 通知公会系统消息
      // 0.3.0-充值(101781-101800)
      MSG_S2C_Recharge_NotifySuccess = 101782; //充值成功通知

      // 0.4.0-神器(101801-101850)
      MSG_C2S_Artifact_UpLevel = 101801; //神器升级
      MSG_S2C_Artifact_UpLevel = 101802;
      MSG_C2S_Artifact_UpStar = 101803; //神器升星
      MSG_S2C_Artifact_UpStar = 101804;
      MSG_C2S_Artifact_Compose_Active = 101805; //神器缘分激活
      MSG_S2C_Artifact_Compose_Active = 101806;
      MSG_C2S_Artifact_Compose_UpLevel = 101807; //神器缘分激活
      MSG_S2C_Artifact_Compose_UpLevel = 101808;
      MSG_C2S_Artifact_Equip = 101809; //神器上阵
      MSG_S2C_Artifact_Equip = 101810;
      MSG_C2S_Artifact_Equip_OneKey = 101811; //神器上阵-一键
      MSG_S2C_Artifact_Equip_OneKey = 101812;

      // 0.4.0-公会BOSS(101851-101870)
      MSG_C2S_GuildBoss_ChallengeBegin = 101851; // 公会BOSS-发起挑战
      MSG_S2C_GuildBoss_ChallengeBegin = 101852;
      MSG_S2C_GuildBoss_ChallengeFinish = 101853; // 公会BOSS-结束挑战
      MSG_C2S_GuildBoss_GetRank = 101854; //公会BOSS-获取公会内个人榜
      MSG_S2C_GuildBoss_GetRank = 101855;
      // 0.4.0-公会(101900-102000)
      MSG_C2S_Guild_Create = 101900;             // 创建公会
      MSG_S2C_Guild_Create = 101901;
      MSG_C2S_Guild_Join = 101902;               // 加入公会
      MSG_S2C_Guild_Join = 101903;
      MSG_C2S_Guild_Quit = 101904;               // 退出公会
      MSG_S2C_Guild_Quit = 101905;
      MSG_C2S_Guild_FastJoin = 101906;            // 快速加入
      MSG_S2C_Guild_FastJoin = 101907;
      MSG_C2S_Guild_EditName = 101908;           // 编辑公会名
      MSG_S2C_Guild_EditName = 101909;
      MSG_C2S_Guild_SetUpgradeStrategy = 101910; // 公会升级方案
      MSG_S2C_Guild_SetUpgradeStrategy = 101911;
      MSG_C2S_Guild_ObtainTaskReward = 101912;   // 领取公会计数奖励
      MSG_S2C_Guild_ObtainTaskReward = 101913;
      MSG_C2S_Guild_ObtainQuestReward = 101914;  // 领取个人任务奖励
      MSG_S2C_Guild_ObtainQuestReward = 101915;
      MSG_C2S_Guild_GetQuestInfo = 101916;       // 获取任务数据
      MSG_S2C_Guild_GetQuestInfo = 101917;
      MSG_C2S_Guild_AssignTitle = 101918;        // 任命职位
      MSG_S2C_Guild_AssignTitle = 101919;
      MSG_C2S_Guild_Kick = 101920;               // 成员被踢出公会
      MSG_S2C_Guild_Kick = 101921;
      MSG_C2S_Guild_InGuild = 101922;            // 设置玩家是否在公会大厅内
      MSG_S2C_Guild_InGuild = 101923;
      MSG_C2S_Guild_DailySign = 101924;          // 公会每日签到
      MSG_S2C_Guild_DailySign = 101925;
      MSG_C2S_Guild_LearnTech = 101926;          // 学习公会科技(升级公会科技节点)
      MSG_S2C_Guild_LearnTech = 101927;
      MSG_C2S_Guild_Search = 101928;             // 公会搜索
      MSG_S2C_Guild_Search = 101929;
      MSG_C2S_Guild_Approve = 101930;            // 批准其加入公会
      MSG_S2C_Guild_Approve = 101931;
      MSG_C2S_Guild_UpspeedTech = 101932;        // 使用道具加速科技升级
      MSG_S2C_Guild_UpspeedTech = 101933;
      MSG_C2S_Guild_Recommend = 101934;          // 公会推荐
      MSG_S2C_Guild_Recommend = 101935;
      MSG_C2S_Guild_GetGuildInfo = 101936;       // 获取公会信息
      MSG_S2C_Guild_GetGuildInfo = 101937;
      MSG_C2S_Guild_Attorn = 101938;             // 转让职位
      MSG_S2C_Guild_Attorn = 101939;
      MSG_C2S_Guild_SetInfo = 101940;            // 设置信息,所有信息同一个协议设置
      MSG_S2C_Guild_SetInfo = 101941;
      MSG_C2S_Guild_OnekeyObtainQuestReward = 101942;  // 一键领取所有玩家个人任务
      MSG_S2C_Guild_OnekeyObtainQuestReward = 101943;
      MSG_C2S_Guild_SetAnnounce = 101944;              // 设置公会宣言
      MSG_S2C_Guild_SetAnnounce = 101945;
      MSG_C2S_Guild_CancelTechUpgrade = 101946;        // 取消科技加速
      MSG_S2C_Guild_CancelTechUpgrade = 101947;
      MSG_C2S_Guild_AssistOther = 101948;        // 协助公会中其它玩家
      MSG_S2C_Guild_AssistOther = 101949;
      MSG_C2S_Guild_ReqAssist = 101950;          // 请求公会中其它玩家协助
      MSG_S2C_Guild_ReqAssist = 101951;
      MSG_C2S_Guild_GetAssistInfo = 101952;      // 获取需要协助玩家列表信息
      MSG_S2C_Guild_GetAssistInfo = 101953;
      MSG_S2C_Guild_NotifyDismiss = 101960;      // 公会自动解散的通知消息
      MSG_S2C_Guild_NotifyJoin = 101961;         // 通知新成员加入
      MSG_S2C_Guild_NotifyQuit = 101962;         // 通知成员主动退出公会
      MSG_S2C_Guild_NotifyUserOnline = 101963;   // 通知公会成员上线
      MSG_S2C_Guild_NotifyEditName = 101964;     // 通知公会名字被修改
      MSG_S2C_Guild_NotifySetUpgradeStrategy = 101965;    // 通知公会升级
      MSG_S2C_Guild_NotifyLearnTech = 101966;    // 通知升级科技
      MSG_S2C_Guild_NotifyUpspeedTech = 101967;  // 通知加速科技
      MSG_S2C_Guild_NotifySignRecord = 101968;   // 通知签到记录
      MSG_S2C_Guild_NotifyAssignTitle = 101969;  // 通知玩家职位被修改
      MSG_S2C_Guild_NotifyKick  = 101970;        // 通知玩家被踢出公会
      MSG_S2C_Guild_NotifyApplyJoin = 101973;    // 通知申请加入
      MSG_S2C_Guild_NotifyDeleteApply = 101974;  // 通知删除申请玩家
      MSG_S2C_Guild_NotifyGuildResourceOp = 101975;  // 通知所有玩家资源有更新
      MSG_S2C_Guild_NotifyAttorn = 101976;       // 通知职位被转让,本质上是职位互换
      MSG_S2C_Guild_NotifySetInfo = 101977;      // 通知设置变化
      MSG_S2C_Guild_NotifySetAnnounce = 101978;  // 通知公会宣言变化
      MSG_S2C_Guild_NotifyApprove = 101979;      // 通知批准
      MSG_S2C_Guild_NotifyGuildLog = 101980;     // 通知公会日志
      MSG_S2C_Guild_NotifyUserOffline = 101981;  // 通知玩家离线
      MSG_S2C_Guild_NotifyCancelTech = 101982;   // 通知取消公会科技
      MSG_S2C_Guild_NotifyAssistMe = 101983;     // 其它玩家协助我,通知我
      MSG_S2C_Guild_NotifyReqAssist = 101984;    // 其它玩家请求协助通知


      // 0.4.0-迷宫（102001-102050）
      MSG_C2S_Rogue_GetInfo = 102001; // 获取迷宫信息
      MSG_S2C_Rogue_GetInfo = 102002;
      MSG_C2S_Rogue_SelectDifficulty = 102003; // 选择难度
      MSG_S2C_Rogue_SelectDifficulty = 102004;
      MSG_C2S_Rogue_SelectCharacter = 102005; // 选择佣兵
      MSG_S2C_Rogue_SelectCharacter = 102006;
      MSG_C2S_Rogue_EnterGrid = 102007; // 进入格子
      MSG_S2C_Rogue_EnterGrid = 102008;
      MSG_C2S_Rogue_ChallengeBegin = 102009; // 挑战
      MSG_S2C_Rogue_ChallengeBegin = 102010;
      MSG_C2S_Rogue_Try = 102011; // 宝箱/掉落/事件
      MSG_S2C_Rogue_Try = 102012;
      MSG_C2S_Rogue_UseItem = 102013; // 使用消耗品
      MSG_S2C_Rogue_UseItem = 102014;
      MSG_C2S_Rogue_SelectAward = 102015; // 奖励领取（1:战斗/2:事件/3:温泉/4:机制）
      MSG_S2C_Rogue_SelectAward = 102016;
      MSG_C2S_Rogue_FlushShop = 102017; // 刷新商店
      MSG_S2C_Rogue_FlushShop = 102018;
      MSG_C2S_Rogue_BuyShop = 102019; // 购买商店
      MSG_S2C_Rogue_BuyShop = 102020;
      MSG_C2S_Rogue_Recruit = 102021; // 招募
      MSG_S2C_Rogue_Recruit = 102022;
      MSG_C2S_Rogue_Wish = 102023; // 心愿单
      MSG_S2C_Rogue_Wish = 102024;
      MSG_C2S_Rogue_RecruitSelect = 102025; // 招募选择
      MSG_S2C_Rogue_RecruitSelect = 102026;
      MSG_C2S_Rogue_UseDevice = 102027; // 使用装置
      MSG_S2C_Rogue_UseDevice = 102028;
      MSG_C2S_Rogue_ActiveTree = 102029; // 激活科技树
      MSG_S2C_Rogue_ActiveTree = 102030;
      MSG_C2S_Rogue_TaskAward = 102031; // 周任务奖励
      MSG_S2C_Rogue_TaskAward = 102032;
      MSG_C2S_Rogue_BookAward = 102033; // 图鉴奖励
      MSG_S2C_Rogue_BookAward = 102034;
      MSG_C2S_Rogue_Quit = 102035; // 退出（结算）
      MSG_S2C_Rogue_Quit = 102036;
      MSG_S2C_Rogue_ChallengeFinish = 102037; // 挑战结束
      MSG_S2C_Rogue_SyncInnerInfo = 102038; // 同步局内数据
      MSG_C2S_Rogue_UseSpring = 102039;   // 使用温泉
      MSG_S2C_Rogue_UseSpring = 102040;
      MSG_C2S_Rogue_DiscardResource = 102041; // 丢弃资源
      MSG_S2C_Rogue_DiscardResource = 102042;
      MSG_S2C_Rogue_SyncBook = 102043; // 同步图鉴信息
      MSG_C2S_Rogue_RetryChallenge = 102044; // 重新挑战
      MSG_S2C_Rogue_RetryChallenge = 102045;
      MSG_S2C_Rogue_TriggerEvent = 102046; // 触发事件（机制）
      MSG_S2C_Rogue_TriggerEventResource = 102047; // 触发事件资源通知

      //0.5.0-日常任务(102051-102070)
      MSG_C2S_DailyQuest_AwardQuest = 102051; //领取任务奖励
      MSG_S2C_DailyQuest_AwardQuest = 102052;
      MSG_C2S_DailyQuest_AwardActive = 102053; //领取活跃奖励
      MSG_S2C_DailyQuest_AwardActive = 102054;

      //0.5.0-战令(102071-102100)
      MSG_S2C_BattlePass_BuyNtf = 102071; //战令购买档位通知
      MSG_C2S_BattlePass_AwardLv = 102072; //战令领取等级奖励
      MSG_S2C_BattlePass_AwardLv = 102073;
      MSG_C2S_BattlePass_BuyLv = 102074; //战令购买等级
      MSG_S2C_BattlePass_BuyLv = 102075;
      MSG_C2S_BattlePass_AwardQuest = 102076; //战令领取任务奖励
      MSG_S2C_BattlePass_AwardQuest = 102077;

      // 0.8.0-迷宫扩展（102101-102150）
      MSG_C2S_Rogue_GetFirstAward = 102103; // 领取首通奖励
      MSG_S2C_Rogue_GetFirstAward = 102104;

      // 0.5.0-小游戏(102201-102250)
      MSG_C2S_CasualGame_EnterGame = 102201;  // 创建新的小游戏
      MSG_S2C_CasualGame_EnterGame = 102202;
      MSG_S2C_CasualGame_NotifyPlayCnt = 102203;   // 通知玩法次数
      MSG_C2S_CasualGame_FinishGame = 102204; // 结束小游戏
      MSG_S2C_CasualGame_FinishGame = 102205;

      // 0.5.0-宝库、割草(102251-102260)
      MSG_C2S_Mow_BeginMow = 102251;         // 开始宝库、割草游戏
      MSG_S2C_Mow_BeginMow = 102252;
      MSG_C2S_Mow_FinishMow = 102253;        // 结算宝库、割草游戏
      MSG_S2C_Mow_FinishMow = 102254;
      MSG_C2S_Mow_Sweep = 102255;            // 宝库、割草扫荡
      MSG_S2C_Mow_Sweep = 102256;

      // 0.5.0-每日特惠(102261-102270)
      MSG_C2S_DailySpecials_Award = 102261; //每日特惠领取
      MSG_S2C_DailySpecials_Award = 102262;
      MSG_S2C_DailySpecials_BuyNtf = 102263; //每日特惠购买通知
      MSG_S2C_DailySpecials_ContinueBuyNtf = 102264; //每日特惠连续购买通知

      // 0.5.0-基金(102271-102280)
      MSG_C2S_Fund_OnekeyObtainReward = 102271;    // 一键领取奖励
      MSG_S2C_Fund_OnekeyObtainReward = 102272;
      MSG_C2S_Fund_ObtainReward = 102273;    // 领取奖励
      MSG_S2C_Fund_ObtainReward = 102274;

      // 0.5.0-首充(102281-102290)
      MSG_C2S_FirstRecharge_Award = 102281; //首充领奖
      MSG_S2C_FirstRecharge_Award = 102282;
      MSG_S2C_FirstRecharge_BuyNtf = 102283; //首充购买通知

      // 0.5.0-累充(102291-102300)
      MSG_C2S_AccumulatedRecharge_Award = 102291; //累充领奖
      MSG_S2C_AccumulatedRecharge_Award = 102292;

      // 0.5.0-月卡(102301-102310)
      MSG_C2S_MonthlyCard_DailyAward = 102301; // 每日领奖
      MSG_S2C_MonthlyCard_DailyAward = 102302;
      MSG_S2C_MonthlyCard_BuyNtf = 102303; // 购买通知

      // 0.5.0-头像&头像框(102311-102320)
      MSG_C2S_Avatar_Set = 102311; // 设置头像
      MSG_S2C_Avatar_Set = 102312;
      MSG_C2S_Avatar_Frame_Set = 102313; // 设置头像框
      MSG_S2C_Avatar_Frame_Set = 102314;

      // 0.5.0-每日签到(1023121-102330)
      MSG_C2S_DailySign_ObtainReward = 102321; // 每日领奖
      MSG_S2C_DailySign_ObtainReward = 102322;

      // 0.5.0-推送礼包(102351-102370)
      MSG_C2S_PushGift_Buy = 102351;      // 推送礼包购买
      MSG_S2C_PushGift_Buy = 102352;
      MSG_S2C_PushGift_NotifyTrigger = 102353;   // 通知触发推送礼包

      // 0.5.0-七日签到(102371-102380)
      MSG_C2S_SevenSign_Award = 102371;    // 七日签到领奖
      MSG_S2C_SevenSign_Award = 102372;

      // 0.6.0-成就(102381-102390)
      MSG_C2S_Achievement_Award = 102381;      // 领取奖励
      MSG_S2C_Achievement_Award = 102382;
      MSG_S2C_Achievement_Notify = 102383;      // 通知成就达成

      // 0.6.0-七日活动(102391-102400)
      MSG_C2S_SevenAct_AwardPoint = 102391; // 积分领奖
      MSG_S2C_SevenAct_AwardPoint = 102392;
      MSG_C2S_SevenAct_AwardQuest = 102393; // 任务领奖
      MSG_S2C_SevenAct_AwardQuest = 102394;

      // 0.8.0-背饰(102421-102460)
      MSG_C2S_Back_Equip = 102421; // 装备背饰
      MSG_S2C_Back_Equip = 102422;
      MSG_C2S_Back_Reset = 102423; // 重置背饰
      MSG_S2C_Back_Reset = 102424;
      MSG_C2S_Back_Decompose = 102425; // 分解背饰
      MSG_S2C_Back_Decompose = 102426;
      MSG_C2S_Back_Lock = 102427; // 背饰上锁
      MSG_S2C_Back_Lock = 102428;
      MSG_C2S_Back_UpgradeLv = 102429; // 背饰升级
      MSG_S2C_Back_UpgradeLv = 102430;
      MSG_C2S_Back_UpgradeStar = 102431; // 背饰升星
      MSG_S2C_Back_UpgradeStar = 102432;
      MSG_C2S_Back_Refresh = 102433; // 刷新背饰商店
      MSG_S2C_Back_Refresh = 102434;
      MSG_C2S_Back_Buy = 102435; // 购买背饰
      MSG_S2C_Back_Buy = 102436;
      MSG_C2S_Back_SetWish = 102437; // 设置心愿
      MSG_S2C_Back_SetWish = 102438;
      MSG_C2S_Back_ActiveBook = 102439; // 激活图鉴
      MSG_S2C_Back_ActiveBook = 102440;
      MSG_C2S_Back_ExpandBag = 102441; // 解锁背包格子
      MSG_S2C_Back_ExpandBag = 102442;

      // 0.9.0-爬塔(102461-102500)
      MSG_C2S_Tower_ChallengeBegin = 102461;                 // 爬塔挑战
      MSG_S2C_Tower_ChallengeBegin = 102462;
      MSG_S2C_Tower_ChallengeFinish = 102463;
      MSG_C2S_Tower_ObtainGlobalFirstPassRewards = 102464;   // 领取服务器首通奖励
      MSG_S2C_Tower_ObtainGlobalFirstPassRewards = 102465;
      MSG_C2S_Tower_FastSweep = 102466;                      // 快速扫荡
      MSG_S2C_Tower_FastSweep = 102467;
      MSG_C2S_Tower_UnlockBuffSlot = 102468;                 // 扩展 Buff 插槽
      MSG_S2C_Tower_UnlockBuffSlot = 102469;
      MSG_C2S_Tower_RefreshBuff = 102470;                    // 刷新 buff
      MSG_S2C_Tower_RefreshBuff = 102471;
      MSG_C2S_Tower_SelectBuff = 102472;                     // 选择 buff
      MSG_S2C_Tower_SelectBuff = 102473;
      MSG_C2S_Tower_SetBuffPefer = 102474;                   // 设置 Buff 偏好
      MSG_S2C_Tower_SetBuffPefer = 102475;
      MSG_S2C_Tower_NotifyServerMaxId = 102476;              // 通知爬塔全服最新关卡 id

      // 0.9.0-佣兵图鉴(102501-102510)
      MSG_C2S_CompanionBook_UpgradeLv = 102501; // 图鉴激活/升级
      MSG_S2C_CompanionBook_UpgradeLv = 102502;

      // 0.9.0-头衔(102511-102520)
      MSG_C2S_Honor_AwardQuest = 102511; // 领取任务
      MSG_S2C_Honor_AwardQuest = 102512;
      MSG_C2S_Honor_Upgrade = 102513; // 晋升
      MSG_S2C_Honor_Upgrade = 102514;

      // 0.9.50-一条龙礼包(102521-102530)
      MSG_C2S_SeriesGift_Buy = 102521;             // 购买一条龙礼包
      MSG_S2C_SeriesGift_Buy = 102522;
      MSG_S2C_SeriesGift_NotifyTrigger = 102523;   // 通知触发了一条龙礼包

      // 0.9.50-每日惊喜福利(102531-102540)
      MSG_C2S_DailySurpriseBenefit_ObtainRewards = 102531;   // 领取每日惊喜福利
      MSG_S2C_DailySurpriseBenefit_ObtainRewards = 102532;

      // 0.9.50-功能预览(102541-102550)
      MSG_C2S_FunctionPreview_ObtainRewards = 102541;   // 领取功能预览奖励
      MSG_S2C_FunctionPreview_ObtainRewards = 102542;

      // 0.9.50-宝库(102551-102560)
      MSG_C2S_Treasury_ChallengeBegin = 102551;   // 开始挑战宝库
      MSG_S2C_Treasury_ChallengeBegin = 102552;
      MSG_S2C_Treasury_ChallengeFinish = 102553;  // 挑战宝库结束
      MSG_C2S_Treasury_Sweep = 102554;            // 扫荡
      MSG_S2C_Treasury_Sweep = 102555;

      // 0.9.50-广告(102561-102570)
      MSG_C2S_Advertise_Use = 102561; // 看广告增加次数，要特殊处理 仅对7|8生效
      MSG_S2C_Advertise_Use = 102562;

      // 0.9.50-礼包码(102571-102580)
      MSG_C2S_GiftCode_Award = 102571; // 礼包码领取
      MSG_S2C_GiftCode_Award = 102572;
            """
    # 按行解析数据
    lines = data_str.strip().split("\n")
    for line in lines:
        # 分割每行数据
        parts = line.strip().split("=")
        if len(parts) != 2:
            continue
        key = parts[0].strip()
        value = parts[1].split(";")[1].strip()

        # 添加到数据字典中
        data[key] = value[2:].strip()
    return data


if __name__ == '__main__':
    main()
