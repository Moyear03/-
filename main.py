from astrbot.api.all import *
from lunar_python import Solar

# 注册插件
# 参数依次为：插件ID, 作者, 描述, 版本
@register("bazi_plugin", "YourName", "专业八字排盘工具", "1.0.0")
class BaziPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    # 注册指令 /bazi
    # 参数类型提示 (year: int) 会自动告诉 AstrBot 如何解析用户输入
    @command("bazi")
    async def bazi(self, event: AstrMessageEvent, year: int, month: int, day: int, hour: int, gender: str = "男"):
        '''
        八字排盘指令
        用法: /bazi 年 月 日 时 [男/女]
        示例: /bazi 2024 2 10 8 男
        '''
        
        try:
            # 1. 初始化阳历对象 (lunar_python 库逻辑)
            solar = Solar.fromYmdHms(year, month, day, hour, 0, 0)
            lunar = solar.getLunar()
            bazi = lunar.getEightChar()
            
            # 2. 处理性别 (lunar_python 中 1=男, 0=女)
            gender_num = 1 if gender == "男" else 0
            bazi.setSek(gender_num) # 设置性别以计算大运

            # 3. 获取四柱
            year_gz = bazi.getYear()
            month_gz = bazi.getMonth()
            day_gz = bazi.getDay()
            time_gz = bazi.getTime()
            
            # 4. 获取五行 (便于知识库分析)
            # 例如：甲木、酉金
            day_master = bazi.getDayGan() # 日干
            moon_cmd = bazi.getMonthZhi() # 月令

            # 5. 计算当前的大运 (简单示例，显示第一步大运)
            yun = bazi.getYun(gender_num)
            # 这里只取起运时间，具体大运排盘比较长，这里做精简展示
            start_yun = yun.getStartSolar().toYmd()

            # 6. 构建回复内容
            result = (
                f"🔮 八字排盘结果\n"
                f"────────────────\n"
                f"📅 公历：{year}年{month}月{day}日 {hour}时\n"
                f"👤 性别：{gender}\n"
                f"────────────────\n"
                f"【乾造/坤造】\n"
                f"年柱：{year_gz}  (属{lunar.getYearShengXiao()})\n"
                f"月柱：{month_gz}\n"
                f"日柱：{day_gz}  (日主: **{day_master}**)\n"
                f"时柱：{time_gz}\n"
                f"────────────────\n"
                f"🚩 起运时间：{start_yun} 前后\n"
                f"🧩 AI 分析提示：\n"
                f"请复制以下指令发送给 AI，以获得《三命通会》解读：\n"
                f"> 分析日主为{day_master}，生于{moon_cmd}月，四柱为{year_gz} {month_gz} {day_gz} {time_gz}的命造。"
            )
            
            # 发送纯文本结果
            yield event.plain_result(result)

        except Exception as e:
            yield event.plain_result(f"❌ 排盘出错，请检查日期格式。\n错误信息: {str(e)}")