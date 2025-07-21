from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

# 创建DeepSeek模型实例
llm = ChatOpenAI(
    model_name="deepseek-chat",  # 指定DeepSeek模型名称
    temperature=0,
    openai_api_base="https://api.deepseek.com/v1",  # DeepSeek的API端点
    openai_api_key="sk-dd2f1a07b52545f0854c65d28996273b"  # 替换为你的DeepSeek API密钥
)

# 创建一个字符串输出解析器
output_parser = StrOutputParser()

# 创建提示模板
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个专业的大数据架构师，请根据用户需求修改内容"),
    ("user", "{input}")
])

# 创建链
chain = prompt | llm | output_parser

# 调用链
result = chain.invoke({"input": '''帮我优化此 SQL：select
distinct c.leibie
,c.fproject_type_name
,count(distinct c.fuid) as cnt --当月分配量
,count(distinct if(c.Fcall_min_pro is not null and date(c.Fcall_min_pro) between '2025-04-01' and '2025-04-10',c.fuid,null)) as call_user_cnt --外呼用户数
,count(distinct if(c.Fcall_connect_min_pro is not null and date(c.Fcall_connect_min_pro) between '2025-04-01' and '2025-04-10',c.fuid,null)) as connect_user_cnt --接通用户数
,count(distinct case when c.Fcall_connect_min_pro is not null and date(c.Fcall_valid_min_pro) between '2025-04-01' and '2025-04-10' then c.fuid end) as valid_connect_user_cnt --有效接通用户数
,count(distinct case when c.Forder_id is not null and c.fis_valid_connect_order=1 and date(c.forder_create_time)  between '2025-04-01' and '2025-04-10' then c.fuid end) as order_succ_user_cnt --下单成功用户数
,count(distinct if(c.Floan_order_succ_flag=1 and c.fis_valid_connect_order=1 and date(c.forder_360_time) between '2025-04-01' and '2025-04-10',c.fuid,null)) as loan_succ_user_cnt --放款成功用户数
,sum(if(c.Floan_order_succ_flag=1 and c.fis_valid_connect_order=1 and date(c.forder_360_time) between '2025-04-01' and '2025-04-10'and c.Fbusiness_own ='借钱',c.Floan_amount,0)) as loan_succ_Floan_amount --放款成功金额
,sum(d.Fcall_valid_pro )  as sc
from (select
fproject_type_name
,case when  Ftemplate_id in("PHJR250403ST162075"
) then "13+在贷" --项目类型/用户群
    when Ftemplate_id in(""
) then "次新降价测试"
    when Ftemplate_id in("PHJR250401ST161622"
,"PHJR250401ST161624"
,"PHJR250401ST161628"
,"PHJR250401ST161626"
,"PHJR250408ST162547"
) then "新转老"
 when Ftemplate_id in(""
) then "次新上迁"
 when Ftemplate_id in("PHJR250407ST162363"
) then "次新"
when Ftemplate_id in(""
) then "M7-12名单"
    when Ftemplate_id in("PHJR250403ST162056"
,"PHJR250403ST162059"
,"PHJR250403ST162053"
,"PHJR250403ST162050"
,"PHJR250410ST162723"
,"PHJR250410ST162729"
,"PHJR250410ST162726"
,"PHJR250410ST162732"
) then "降价测试"
when Ftemplate_id in(""
) then "重授信"
when Ftemplate_id in(""
) then "提还调研"
when Ftemplate_id in(""
) then "潜客高通有券"
when Ftemplate_id in(""
) then "潜客高通无券"
when Ftemplate_id in(""
) then "提额名单"
when Ftemplate_id in("PHJR250401ST161668"
) then "潜客专项"
when Ftemplate_id in("PHJR250403ST162068"
,"PHJR250403ST162071"
,"PHJR250403ST162065"
,"PHJR250403ST162062"
) then "潜客降价测试"
when Ftemplate_id in("PHJR250401ST161613"
,"PHJR241218ST141770"
,"PHJR241218ST141770"
,"PHJR250402ST161683"
) then "常规名单"
when Ftemplate_id in(""
) then "临转固"

end as leibie
,fuid
,Fcall_min_pro
,Fcall_connect_min_pro
,Fcall_valid_min_pro
,Forder_id
,fis_valid_connect_order
,forder_create_time
,Floan_order_succ_flag
,forder_360_time
,Floan_amount
,Fbusiness_own
from dp_kf_mart.dm_kf_tel_whole_path_order_detail_df_v2
where f_p_date between '2025-04-01' and '2025-04-10'
and Fbusiness_type_name ='普惠'

and fseat_type_md='BPO'
)c
left join
 (
    select distinct fuid
    ,count(distinct case when Fis_valid_call='1' and Fcall_duration>=30 then Fcall_id end) as Fcall_valid_pro     --有效通话次数
   from dp_kf_mart.dm_dx_call_detail_day
    where Fseat_type<>'微信'
    and Fis_valid_call='1'
    and Fdis_group like '%普惠%'

    and date(Fcall_created_time) between '2025-04-01' and '2025-04-10'
    group by fuid
    )d
    on c.fuid=d.fuid
group by c.leibie,c.fproject_type_name
order by c.leibie,c.fproject_type_name
 limit 100'''})
print(result)