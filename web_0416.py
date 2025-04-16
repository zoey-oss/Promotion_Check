import streamlit as st
import pandas as pd
import io
from promotion_logic_0416 import promotion_check

# Set page configuration
st.set_page_config(
    page_title="员工晋升资格评估工具",
    page_icon="📊",
    layout="wide"
)

# Application title and description
st.title("员工晋升资格评估工具")
st.markdown("""
此应用程序根据公司晋升规则评估员工晋升资格。上传包含员工数据的Excel文件，应用程序将添加晋升资格结果。
""")

# File upload section
st.header("上传员工数据")
uploaded_file = st.file_uploader("选择Excel文件", type=["xlsx", "xls"])

# Function to validate required columns
def validate_data(df):
    required_columns = ['当前职级', '本次绩效', '上次绩效', '司龄', '是否带团队']
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    if missing_columns:
        return False, f"Excel文件缺少必要列: {', '.join(missing_columns)}"
    
    # Check that performance values are valid
    valid_performance = ['M', 'M+', 'E', 'O']
    invalid_curr_perf = df[~df['本次绩效'].isin(valid_performance)]['本次绩效'].unique()
    invalid_last_perf = df[~df['上次绩效'].isin(valid_performance)]['上次绩效'].unique()
    
    if len(invalid_curr_perf) > 0:
        return False, f"本次绩效包含无效值: {', '.join(map(str, invalid_curr_perf))}。有效值为: {', '.join(valid_performance)}"
    
    if len(invalid_last_perf) > 0:
        return False, f"上次绩效包含无效值: {', '.join(map(str, invalid_last_perf))}。有效值为: {', '.join(valid_performance)}"
    
    # Check that is_leader values are valid
    valid_leader = ['Y', 'N']
    invalid_leader = df[~df['是否带团队'].isin(valid_leader)]['是否带团队'].unique()
    
    if len(invalid_leader) > 0:
        return False, f"是否带团队包含无效值: {', '.join(map(str, invalid_leader))}。有效值为: {', '.join(valid_leader)}"
    
    return True, ""

# Function to process the data
def process_data(df):
    # Create a copy to avoid modifying the original dataframe
    results_df = df.copy()
    
    # Add a new column for promotion results
    results_df['晋升结果'] = results_df.apply(
        lambda row: promotion_check(
            row['当前职级'], 
            row['本次绩效'], 
            row['上次绩效'], 
            row['司龄'], 
            row['是否带团队']
        ), 
        axis=1
    )
    
    return results_df

# Main processing logic
if uploaded_file is not None:
    try:
        st.info("正在处理数据，请稍等...")
        
        # Load the Excel file
        df = pd.read_excel(uploaded_file)
        
        # Display the original data
        st.subheader("原始数据预览")
        st.dataframe(df.head())
        
        # Validate the data
        is_valid, error_message = validate_data(df)
        
        if is_valid:
            # Process the data
            results_df = process_data(df)
            
            # Display the results
            st.subheader("处理结果预览")
            st.dataframe(results_df)
            
            # Generate summary statistics
            st.subheader("晋升结果统计")
            promotion_counts = results_df['晋升结果'].value_counts()
            st.bar_chart(promotion_counts)
            
            # Prepare the Excel file for download
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                results_df.to_excel(writer, index=False)
            
            # Offer download button
            st.download_button(
                label="下载处理结果",
                data=output.getvalue(),
                file_name="晋升结果.xlsx",
                mime="application/vnd.ms-excel"
            )
            
            # Display detailed analysis
            st.subheader("详细分析")
            
            # Analysis by current position
            st.write("按当前职级的晋升结果分布")
            position_results = pd.crosstab(results_df['当前职级'], results_df['晋升结果'])
            st.dataframe(position_results)
            
            # Analysis by leadership status
            st.write("按是否带团队的晋升结果分布")
            leader_results = pd.crosstab(results_df['是否带团队'], results_df['晋升结果'])
            st.dataframe(leader_results)
            
            # Analysis by performance
            st.write("按绩效组合的晋升结果分布")
            perf_results = pd.crosstab(
                index=[results_df['本次绩效'], results_df['上次绩效']],
                columns=results_df['晋升结果']
            )
            st.dataframe(perf_results)
            
        else:
            st.error(error_message)
            
    except Exception as e:
        st.error(f"处理数据时出错: {str(e)}")
else:
    # Instructions when no file is uploaded
    st.info("请上传Excel文件以开始处理。")
    
    # Show expected format
    st.subheader("Excel文件格式说明")
    st.markdown("""
    上传的Excel文件必须包含以下列:
    
    1. **当前职级**: 员工当前的职级 (例如 I1-1, E1-2 等)
    2. **本次绩效**: 当前评估周期的绩效评级 (M, M+, E, O)
    3. **上次绩效**: 上一评估周期的绩效评级 (M, M+, E, O)
    4. **司龄**: 员工在公司工作的年数 (例如 1.5 表示一年半)
    5. **是否带团队**: 员工是否担任领导角色 (Y 或 N)
    
    示例:
    
    | 员工ID | 姓名 | 当前职级 | 本次绩效 | 上次绩效 | 司龄 | 是否带团队 |
    |--------|------|----------|----------|----------|------|------------|
    | 001    | 张三 | I2-1     | M+       | M        | 1.5  | N          |
    | 002    | 李四 | E1-1     | E        | M+       | 2.0  | Y          |
    """)

# Footer
st.markdown("---")
st.markdown("© 2023 员工晋升资格评估工具")