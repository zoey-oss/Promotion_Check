def promotion_check(cur_position, cur_performance, last_performance, work_year, if_leader):
    performance = ['M','M+','E', 'O']
    # mmm=        [0,      1       2      3      4      5      6       7     8       9      10     11     12     13    14    15   16]
    prof_rank = ['I1-1','I1-2','I2-1','I2-2','I2-3','I3-1','I3-2','I3-3','I4-1','I4-2','I4-3','I5-1','I5-2','I6-1','I6-2','I7','I8']
    mana_rank = ['E1-1','E1-2','E2-1','E2-2','E3-1','E3-2','E3-3','E3-4','E4-1','E4-2','E5','E6','E7']
    # 晋升绩效条件
    curmm_lastm = cur_performance in performance[1:]   #本次M+，上次M
    both_mm = cur_performance in performance[1:] and last_performance in performance[1:]  #两次M+
    mm_plus_e = (cur_performance in performance[1:] and last_performance in performance[2:]) or \
                    (cur_performance in performance[2:] and last_performance in performance[1:])     #一次M+一次E
    both_e = cur_performance in performance[2:] and last_performance in performance[2:]   #两次E
    curo_lastmm = cur_performance == 'O' and last_performance in performance[1:]  #本O上E
    e_plus_o = (cur_performance in performance[2:] and last_performance in performance == 'O') or \
                    (cur_performance == 'O' and last_performance in performance[2:])     #一次O一次E
    curo_lastmm = cur_performance == 'O' and last_performance in performance[1:]  #本O上M+
    mm_plus_o = (cur_performance in performance[1:] and last_performance == 'O') or \
                    (cur_performance == 'O' and last_performance in performance[1:])     #一次M+一次O(管理升专业，可能有问题)

    #话术
    normal_speed = '可（正常）逐级晋升至——'
    fast_speed = '可（快速）逐级晋升至——'
    cross_speed = '可跨级晋升至——'
    fail_result = '绩效不达标'
    time_nenough = '在职时长不够'
    both_fail = '绩效不达标且在职时长不够'

    #专业晋升
    if if_leader == 'N':
        # result1 = prof_rank[prof_rank.index(cur_position)+1]
        # result2 = prof_rank[prof_rank.index(cur_position)+2]
        
        if cur_position in prof_rank[:3]:
            if work_year >= 0.5:
                if mm_plus_e:
                    return cross_speed + prof_rank[prof_rank.index(cur_position)+2]

                elif curmm_lastm:
                    return normal_speed + prof_rank[prof_rank.index(cur_position)+1]
                
                else:
                    return fail_result
                
            else:
                if mm_plus_e or curmm_lastm:
                    return time_nenough
                else:
                    return both_fail
                
        elif cur_position in prof_rank[3:9]:
            if work_year >= 0.5 and e_plus_o:
                    return cross_speed + prof_rank[prof_rank.index(cur_position)+2]
            
            elif cur_position == 'I2-2':
                if work_year >= 0.5:
                    if mm_plus_e :
                        return normal_speed + prof_rank[prof_rank.index(cur_position)+1]
                    else:
                        return fail_result    
                else:
                    if mm_plus_e:
                        return time_nenough
                    else:
                        return both_fail
            
            elif cur_position == 'I2-3':
                if mm_plus_e and work_year >= 0.5:
                    return fast_speed + prof_rank[prof_rank.index(cur_position)+1]
                elif work_year >= 1:
                    if both_mm:
                        return normal_speed + prof_rank[prof_rank.index(cur_position)+1]
                    else:
                        return fail_result
                    
                elif work_year < 1:
                    if both_mm:
                        return time_nenough
                    else:
                        return both_fail
            
            elif cur_position in prof_rank[5:7]:
                if work_year >= 0.5:
                    if both_mm:
                        return normal_speed + prof_rank[prof_rank.index(cur_position)+1]
                    else:
                        return fail_result
                    
                else:
                    if both_mm:
                        return time_nenough
                    else:
                        return both_fail
                
            elif cur_position == 'I3-3':
                if mm_plus_e and work_year >= 0.5:
                    return fast_speed + prof_rank[prof_rank.index(cur_position)+1]
                elif work_year >= 1:
                    if both_mm:
                        return normal_speed + prof_rank[prof_rank.index(cur_position)+1]
                    else:
                        return fail_result
                elif work_year < 1:
                    if both_mm:
                        return time_nenough
                    else:
                        return both_fail
                
            elif cur_position == 'I4-1':
                if mm_plus_e and work_year >= 0.5:
                    return fast_speed + prof_rank[prof_rank.index(cur_position)+1]
                elif work_year >= 0.5:
                    if both_mm:
                        return normal_speed + prof_rank[prof_rank.index(cur_position)+1]
                    else:
                        return fail_result
                elif work_year < 0.5:
                    if both_mm:
                        return time_nenough
                    else:
                        return both_fail
                
        elif cur_position in prof_rank[9:10]:
            if work_year >= 0.5:
                if both_mm:
                    return normal_speed + prof_rank[prof_rank.index(cur_position)+1]
                else:
                    return fail_result
            else:
                if both_mm:
                    return time_nenough
                else:
                    return both_fail
            
        elif cur_position in prof_rank[10:12]:
            if e_plus_o and work_year >= 0.5:
                return fast_speed + prof_rank[prof_rank.index(cur_position)+1]
            elif work_year >= 1:
                if mm_plus_e:
                    return normal_speed + prof_rank[prof_rank.index(cur_position)+1]
                else:
                    return fail_result
            elif work_year < 1:
                if mm_plus_e:
                    return time_nenough
                else:
                    return both_fail
            
        elif cur_position in prof_rank[12:15]:
            if e_plus_o and work_year >= 1:
                return fast_speed + prof_rank[prof_rank.index(cur_position)+1]
            elif work_year >= 1.5:
                if both_e:
                    return normal_speed + prof_rank[prof_rank.index(cur_position)+1]
                else:
                    return fail_result
            elif work_year < 1.5:
                if both_e:
                    return time_nenough
                else:
                    return both_fail
            
        elif cur_position == 'I7':
            if e_plus_o and work_year >= 2:
                return fast_speed + prof_rank[prof_rank.index(cur_position)+1]
            elif work_year >= 3:
                if both_e:
                    return normal_speed + prof_rank[prof_rank.index(cur_position)+1]
                else:
                    return fail_result
            elif work_year < 3:
                if both_e:
                    return time_nenough
                else:
                    return both_fail

        elif cur_position == 'I8':
            return '无晋升'
        
        elif cur_position == 'E1-1':
            if mm_plus_o and work_year >= 1:
                return cross_speed + 'I4-1'
            elif work_year >= 1:
                if both_mm:
                    return normal_speed + 'I3-3'
                else:
                    return fail_result
            elif work_year < 1:
                if both_mm:
                    return time_nenough
                else:
                    return both_fail

        elif cur_position == 'E1-2':
            if mm_plus_o and work_year >= 1:
                return cross_speed + 'I4-2'
            elif work_year >= 1:
                if both_mm:
                    return normal_speed + 'I4-1'
                else:
                    return fail_result
            elif work_year < 1:
                if both_mm:
                    return  time_nenough
                else:
                    return both_fail

        elif cur_position == 'E2-1':
            if work_year >= 1:
                if mm_plus_e:
                    return normal_speed + 'I5-1'
                else:
                    return fail_result
            else:
                if mm_plus_e:
                    return time_nenough
                else:
                    return both_fail
 
        elif cur_position in mana_rank[3:]:
            return '职级与是否带团队不匹配'
            
    # 管理晋升
    if if_leader == 'Y':
        if cur_position == 'E1-1':
            if (both_e or curo_lastmm) and work_year >= 1.5:
                return cross_speed + mana_rank[mana_rank.index(cur_position)+2]
            elif work_year >= 1:
                if mm_plus_e:
                    return normal_speed + mana_rank[mana_rank.index(cur_position)+1]
                else:
                    return fail_result
            elif work_year < 1:
                if mm_plus_e:
                    return time_nenough
                else:
                    return both_fail
                    
        elif cur_position == 'E1-2':
            if work_year >= 1:
                if mm_plus_e:
                    return normal_speed + mana_rank[mana_rank.index(cur_position)+1]
                else:
                    return fail_result
            elif work_year < 1:
                if mm_plus_e:
                    return time_nenough
                else:
                    return both_fail

        elif cur_position in mana_rank[2:6]:
            if work_year >= 2:
                if both_e or curo_lastmm:
                    return normal_speed + mana_rank[mana_rank.index(cur_position)+1]
                else:
                    return fail_result
            else:
                if both_e or curo_lastmm:
                    return time_nenough
                else:
                    return both_fail
        elif cur_position in mana_rank[6:]:
            return '不知道如何晋升'
                
        elif cur_position == 'I2-3':
            if work_year >= 1:
                if mm_plus_e:
                    return normal_speed + 'E1-1'
                else:
                    return fail_result
            else:
                if mm_plus_e:
                    return time_nenough
                else:
                    return both_fail         

        elif cur_position in prof_rank[5:8]:
            if work_year >= 0.5:
                if mm_plus_e:
                    return normal_speed + 'E1-2'
                else:
                    return fail_result  
            else:
                if mm_plus_e:
                    return time_nenough
                else:
                    return both_fail
                
        elif cur_position in prof_rank[8:]:
            if work_year >= 0.5:
                if both_e:
                    if cur_position in prof_rank[8:11]:
                        return normal_speed + 'E2-1'
                    elif cur_position in prof_rank[11:13]:
                        return normal_speed + 'E2-2'
                    elif cur_position in prof_rank[13:15]:
                        return normal_speed + 'E3-1'
                    elif cur_position in prof_rank[15]:
                        return normal_speed + 'E3-2'
                    else:
                        return normal_speed + 'E3-3'
                else:
                    return fail_result
            else:
                if both_e:
                    return time_nenough
                else:
                    return both_fail
                
        elif cur_position in prof_rank[:4]:
            return '职级与是否带团队不匹配'
        

