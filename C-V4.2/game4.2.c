// Doki doki Ohayou Sayori!游戏主程序v4.2
#include <stdio.h>      
#include <windows.h>    
#include <string.h>     
#include <stdlib.h>     
#include <time.h>       

#define MAX_SAVES 15
// 成就系统相关常量
#define MAX_ACHIEVEMENTS 10
#define MAX_UNLOCKABLES 10
#define MAX_CONDITIONS 15

// 全局变量声明
int g_strange = 0;
int g_attention = 0;

// 文本系统全局设置
int g_text_speed = 10;
int g_display_mode = 0;

// 自动存档全局变量
int g_auto_save_enabled = 1;
int g_auto_save_slot = MAX_SAVES - 1;
int g_last_auto_save_chapter = 0;

// 暂停菜单控制变量
int g_return_to_menu = 0;

// 成就系统全局变量
struct Achievement {
    char id[50];
    char name[100];
    char description[200];
    char hint[300];
    int completed;
    int condition_count;
    char condition_ids[MAX_CONDITIONS][50];
    int conditions[MAX_CONDITIONS];
    char unlockable_id[50];
};

struct Unlockable {
    char id[50];
    char title[100];
    char filename[50];
    int unlocked;
};

struct Achievement g_achievements[MAX_ACHIEVEMENTS];
struct Unlockable g_unlockables[MAX_UNLOCKABLES];
int g_achievement_count = 0;
int g_unlockable_count = 0;

// 存档数据结构
struct SaveData {
    int chapter;
    int strange;
    int attention;
    char saveTime[20];
    char preview[100];
    int text_speed;
    int display_mode;
};

struct Choice{
    char prompt[100];
    char option[10][100];
    int aimchapter[20];
    int optioncount;
};

struct SaveData saves[MAX_SAVES];
int saveCount = 0;

// 函数声明
void set_text_color(int color);
void flash_screen(int times);
void LOAD_ALL_SAVES();
int LOAD_GAME_MENU();
void SAVE_GAME(int currentChapter, const char* lastText);
void AUTO_SAVE(int currentChapter, const char* lastText);
int SELECT(struct Choice* choice);
void SP(const char* text, int base_sleeptime_ms);
void STORY(const char* filename, int startchapter);
void SHOW_WELCOME();
void TEXT_SETTINGS_MENU();
void PAUSE_MENU(int currentChapter, const char* lastText);

// ==================== 成就系统函数声明 ====================
void INIT_ACHIEVEMENTS();
int LOAD_ACHIEVEMENTS();
void SAVE_ACHIEVEMENTS();
void UPDATE_ACHIEVEMENT_CONDITION(const char* condition_id);
void ACHIEVEMENT_MENU();
void SHOW_ACHIEVEMENTS();
void SHOW_UNLOCKABLES();
void PLAY_UNLOCKABLE(int index);
void SIMPLE_STORY(const char* filename, int startchapter);

// ==================== 成就系统实现 ====================

// 初始化成就系统
void INIT_ACHIEVEMENTS() {
    // 先尝试加载已有的成就数据
    if(!LOAD_ACHIEVEMENTS()) {
        // 如果加载失败（第一次运行），初始化默认成就
        
        // 成就1
        strcpy(g_achievements[0].id, "ACHIEVEMENT_1");
        strcpy(g_achievements[0].name, "成就1：抱抱能量！");
        strcpy(g_achievements[0].description, "最喜欢sayori啦！");
        strcpy(g_achievements[0].hint, "需要完成所有关于拥抱的剧情。奖励小剧场1。");
        g_achievements[0].completed = 0;
        g_achievements[0].condition_count = 15;

        // 一行循环搞定15个条件！
        for(int i = 0; i < g_achievements[0].condition_count; i++) {
            sprintf(g_achievements[0].condition_ids[i], "拥抱%d", i + 1);
            g_achievements[0].conditions[i] = 0;
        }
        // 删除下面这个多余的循环
        strcpy(g_achievements[0].unlockable_id, "UNLOCKABLE_1");
        
        // 成就2
        strcpy(g_achievements[1].id, "ACHIEVEMENT_2");
        strcpy(g_achievements[1].name, "成就2：学在脚大！");
        strcpy(g_achievements[1].description, "孵蛋孵蛋蛋孵蛋~日月光华同灿烂~");
        strcpy(g_achievements[1].hint, "需要完成所有关于具体的脚大地点的剧情。奖励小剧场2。");
        g_achievements[1].completed = 0;
        g_achievements[1].condition_count = 7;
        
        for(int i = 0; i < g_achievements[1].condition_count; i++) {
            sprintf(g_achievements[1].condition_ids[i], "脚大%d", i + 1);
            g_achievements[1].conditions[i] = 0;
        }
        // 删除下面这个多余的循环
        strcpy(g_achievements[1].unlockable_id, "UNLOCKABLE_2");
        
        // 成就3
        strcpy(g_achievements[2].id, "ACHIEVEMENT_3");
        strcpy(g_achievements[2].name, "成就3：现在，大家都开心了？");
        strcpy(g_achievements[2].description, "恶趣味：在原版DDLC中，如果试图开局作弊删掉sayori.chr或者monika.chr，Sayori就会立即死亡，十分钟后屏幕出现Now, everyone is happy.");
        strcpy(g_achievements[2].hint, "需要完成主线的所有结局。奖励小剧场3。");
        g_achievements[2].completed = 0;
        g_achievements[2].condition_count = 9;
        
        for(int i = 0; i < g_achievements[2].condition_count; i++) {
            sprintf(g_achievements[2].condition_ids[i], "结局%d", i + 1);
            g_achievements[2].conditions[i] = 0;
        }
        // 删除下面这个多余的循环
        strcpy(g_achievements[2].unlockable_id, "UNLOCKABLE_3");
        
        // 小剧场1
        strcpy(g_unlockables[0].id, "UNLOCKABLE_1");
        strcpy(g_unlockables[0].title, "小剧场1：有朋自远方来");
        strcpy(g_unlockables[0].filename, "playoff_1.txt");
        g_unlockables[0].unlocked = 0;
        
        // 小剧场2
        strcpy(g_unlockables[1].id, "UNLOCKABLE_2");
        strcpy(g_unlockables[1].title, "小剧场2：假装游刃有余的一天");
        strcpy(g_unlockables[1].filename, "playoff_2.txt");
        g_unlockables[1].unlocked = 0;
        
        // 小剧场3
        strcpy(g_unlockables[2].id, "UNLOCKABLE_3");
        strcpy(g_unlockables[2].title, "小剧场3：孤独的守望");
        strcpy(g_unlockables[2].filename, "playoff_3.txt");
        g_unlockables[2].unlocked = 0;
        
        g_achievement_count = 3;
        g_unlockable_count = 3;
        
        // 保存初始成就数据
        SAVE_ACHIEVEMENTS();
    }
}

// 加载成就数据
int LOAD_ACHIEVEMENTS() {
    FILE* file = fopen("achievements.dat", "rb");
    if(file) {
        fread(&g_achievement_count, sizeof(int), 1, file);
        fread(&g_unlockable_count, sizeof(int), 1, file);
        
        for(int i = 0; i < g_achievement_count; i++) {
            fread(&g_achievements[i], sizeof(struct Achievement), 1, file);
        }
        
        for(int i = 0; i < g_unlockable_count; i++) {
            fread(&g_unlockables[i], sizeof(struct Unlockable), 1, file);
        }
        
        fclose(file);
        return 1;
    }
    return 0;
}

// 保存成就数据
void SAVE_ACHIEVEMENTS() {
    FILE* file = fopen("achievements.dat", "wb");
    if(file) {
        fwrite(&g_achievement_count, sizeof(int), 1, file);
        fwrite(&g_unlockable_count, sizeof(int), 1, file);
        
        for(int i = 0; i < g_achievement_count; i++) {
            fwrite(&g_achievements[i], sizeof(struct Achievement), 1, file);
        }
        
        for(int i = 0; i < g_unlockable_count; i++) {
            fwrite(&g_unlockables[i], sizeof(struct Unlockable), 1, file);
        }
        
        fclose(file);
    }
}

// 更新成就条件
void UPDATE_ACHIEVEMENT_CONDITION(const char* condition_id) {
    for(int i = 0; i < g_achievement_count; i++) {
        int condition_index = -1;
        for(int j = 0; j < g_achievements[i].condition_count; j++) {
            if(strcmp(g_achievements[i].condition_ids[j], condition_id) == 0) {
                condition_index = j;
                break;
            }
        }
        
        if(condition_index != -1 && !g_achievements[i].conditions[condition_index]) {
            g_achievements[i].conditions[condition_index] = 1;
            printf("✓ 达成条件: %s\n", condition_id);
            
            int all_conditions_met = 1;
            for(int j = 0; j < g_achievements[i].condition_count; j++) {
                if(!g_achievements[i].conditions[j]) {
                    all_conditions_met = 0;
                    break;
                }
            }
            
            if(all_conditions_met && !g_achievements[i].completed) {
                g_achievements[i].completed = 1;
                printf("\n🎉 成就解锁：%s！\n", g_achievements[i].name);
                
                for(int k = 0; k < g_unlockable_count; k++) {
                    if(strcmp(g_unlockables[k].id, g_achievements[i].unlockable_id) == 0) {
                        g_unlockables[k].unlocked = 1;
                        printf("✨ 已解锁小剧场：%s\n", g_unlockables[k].title);
                    }
                }
            }
            
            SAVE_ACHIEVEMENTS();
            break;
        }
    }
}

// 成就系统主菜单
void ACHIEVEMENT_MENU() {
    int choice;
    do {
        printf("\n======= 成就系统 =======\n");
        printf("1. 查看成就\n");
        printf("2. 小剧场\n");
        printf("3. 返回主菜单\n");
        printf("请选择: ");
        
        if(scanf("%d", &choice) != 1) {
            while(getchar() != '\n');
            choice = 0;
            continue;
        }
        while(getchar() != '\n');
        
        switch(choice) {
            case 1:
                SHOW_ACHIEVEMENTS();
                break;
            case 2:
                SHOW_UNLOCKABLES();
                break;
            case 3:
                printf("返回主菜单...\n");
                break;
            default:
                printf("无效选择！\n");
        }
    } while(choice != 3);
}

// 显示成就列表
void SHOW_ACHIEVEMENTS() {
    printf("\n======= 成就列表 =======\n");
    for(int i = 0; i < g_achievement_count; i++) {
        printf("%d. %s\n", i+1, g_achievements[i].name);
        if(g_achievements[i].completed) {
            printf("   ✅ 已完成！\n");
            printf("   %s\n", g_achievements[i].description);
        } else {
            printf("   ❌ 未完成\n");
            printf("   进度: ");
            int completed_count = 0;
            for(int j = 0; j < g_achievements[i].condition_count; j++) {
                if(g_achievements[i].conditions[j]) {
                    printf("✅");
                    completed_count++;
                } else {
                    printf("⬜");
                }
            }
            printf(" (%d/%d)\n", completed_count, g_achievements[i].condition_count);
            printf("   提示: %s\n", g_achievements[i].hint);
        }
        printf("\n");
    }
    printf("按回车键继续...");
    getchar();
}

// 显示小剧场列表
void SHOW_UNLOCKABLES() {
    printf("\n======= 小剧场 =======\n");
    int has_unlocked = 0;
    
    for(int i = 0; i < g_unlockable_count; i++) {
        if(g_unlockables[i].unlocked) {
            has_unlocked = 1;
            printf("%d. %s\n", i+1, g_unlockables[i].title);
        }
    }
    
    if(!has_unlocked) {
        printf("暂无解锁的小剧场\n");
        printf("完成成就来解锁更多内容！\n");
        printf("按回车键继续...");
        getchar();
        return;
    }
    
    printf("%d. 返回\n", g_unlockable_count + 1);
    printf("请选择小剧场: ");
    
    int choice;
    if(scanf("%d", &choice) == 1) {
        while(getchar() != '\n');
        if(choice > 0 && choice <= g_unlockable_count) {
            PLAY_UNLOCKABLE(choice - 1);
        }
    }
}

// 播放小剧场
void PLAY_UNLOCKABLE(int index) {
    if(index < 0 || index >= g_unlockable_count || !g_unlockables[index].unlocked) {
        printf("无法播放该小剧场！\n");
        return;
    }
    
    printf("\n开始播放小剧场：%s\n", g_unlockables[index].title);
    printf("按回车键开始...\n");
    getchar();
    
    // 调用简化版故事播放器
    SIMPLE_STORY(g_unlockables[index].filename, 1);
}

// 简化版故事播放器 - 专门用于小剧场
void SIMPLE_STORY(const char* filename, int startchapter) {
    FILE* file = fopen(filename, "r");
    if(!file) {
        printf("错误！无法打开小剧场文件：%s\n", filename);
        return;
    }

    printf("\n======= 小剧场开始 =======\n");
    
    char line[1500];
    int currentchapter = startchapter;
    int foundcurrentchapter = 0;

    while(fgets(line, sizeof(line), file)) {
        line[strcspn(line, "\n")] = 0;
        if (line[0]=='#'||line[0]=='\0') {
            continue;
        }

        int chapter;
        char character[50], text[1500];
        if(sscanf(line, "%d,%[^,],%[^\n]", &chapter, character, text) == 3) {
            if (chapter < currentchapter) {
                continue;
            }
            if (chapter > currentchapter) {
                break;
            }

            foundcurrentchapter = 1;

            // 处理特效指令
            if(strcmp(character, "effect") == 0) {
                if(strncmp(text, "color ", 6) == 0) {
                    int color = atoi(text+6);
                    set_text_color(color);
                }
                else if(strncmp(text, "flash ", 6) == 0) {
                    int times = atoi(text+6);
                    flash_screen(times);
                }
                continue;
            }
            
            // 处理跳转指令
            if(strcmp(character, "jump") == 0) {
                currentchapter = atoi(text);
                // 重置文件指针到开头，重新读取
                fseek(file, 0, SEEK_SET);
                foundcurrentchapter = 0;
                continue;
            }

            // 显示角色和文本
            printf("[%s]: ", character);
            SP(text, g_text_speed);

            // 等待用户按回车继续
            printf("按回车继续...");
            getchar();
        }
    }
    fclose(file);

    if(!foundcurrentchapter) {
        printf("小剧场内容为空或未找到。\n");
    }

    printf("\n======= 小剧场结束 =======\n");
    printf("按回车返回成就菜单...");
    getchar();
}

// ==================== 原有游戏函数实现 ====================

// 加载所有存档函数
void LOAD_ALL_SAVES() {
    for(int i = 0; i < MAX_SAVES; i++) {
        char filename[20];
        sprintf(filename, "save%d.dat", i+1);
        
        FILE* file = fopen(filename, "rb");
        if(file) {
            fread(&saves[i], sizeof(struct SaveData), 1, file);
            fclose(file);
            saveCount++;
        } else {
            saves[i].chapter = 0;
            saves[i].strange = 0;
            saves[i].attention = 0;
            strcpy(saves[i].saveTime, "");
            strcpy(saves[i].preview, "");
            saves[i].text_speed = 10;
            saves[i].display_mode = 0;
        }
    }
}

// 加载游戏菜单
int LOAD_GAME_MENU() {
    printf("\n======= 选择存档 =======\n");
    int validSaves = 0;
    int validIndices[MAX_SAVES];
    
    for(int i = 0; i < MAX_SAVES; i++) {
        if(saves[i].chapter > 0) {
            printf("%d. [存档位%d] 第%d章 - %s\n", 
                   validSaves+1, i+1, saves[i].chapter, saves[i].saveTime);
            printf("   预览: %.50s%s\n", saves[i].preview, 
                   strlen(saves[i].preview) > 50 ? "..." : "");
            validIndices[validSaves] = i;
            validSaves++;
        }
    }
    
    if(validSaves == 0) {
        printf("没有找到存档！\n");
        return -1;
    }
    
    printf("%d. 返回主菜单\n", validSaves+1);
    
    int choice;
    do {
        printf("请选择存档 (1-%d): ", validSaves+1);
        if(scanf("%d", &choice) != 1) {
            while(getchar() != '\n');
            choice = 0;
        }
    } while(choice < 1 || choice > validSaves+1);
    
    if(choice == validSaves+1) {
        return -1;
    }
    
    return validIndices[choice-1];
}

// 保存游戏函数
void SAVE_GAME(int currentChapter, const char* lastText) {
    printf("\n======= 选择存档位 =======\n");
    for(int i = 0; i < MAX_SAVES; i++) {
        if(saves[i].chapter == 0) {
            printf("%d. [存档位%d] [空存档位]\n", i+1, i+1);
        } else {
            char auto_save_marker[] = "[自动存档]";
            char* is_auto_save = strstr(saves[i].preview, auto_save_marker);
            
            printf("%d. [存档位%d] 第%d章 - %s %s\n", 
                   i+1, i+1, saves[i].chapter, saves[i].saveTime,
                   is_auto_save ? "(自动存档)" : "(手动存档)");
        }
    }
    
    int slot;
    do {
        printf("请选择存档位 (1-%d): ", MAX_SAVES);
        if(scanf("%d", &slot) != 1) {
            while(getchar() != '\n');
            slot = 0;
        }
    } while(slot < 1 || slot > MAX_SAVES);
    
    slot--;
    saves[slot].chapter = currentChapter;
    saves[slot].strange = g_strange;
    saves[slot].attention = g_attention;
    saves[slot].text_speed = g_text_speed;
    saves[slot].display_mode = g_display_mode;
    
    time_t now = time(NULL);
    struct tm* timeinfo = localtime(&now);
    strftime(saves[slot].saveTime, 20, "%Y-%m-%d %H:%M", timeinfo);
    
    strncpy(saves[slot].preview, lastText, 99);
    saves[slot].preview[99] = '\0';
    
    char filename[20];
    sprintf(filename, "save%d.dat", slot+1);
    FILE* file = fopen(filename, "wb");
    if(file) {
        fwrite(&saves[slot], sizeof(struct SaveData), 1, file);
        fclose(file);
        printf("游戏已手动存档到 存档位%d！\n", slot+1);
    } else {
        printf("存档失败！无法创建文件。\n");
    }
    
    while(getchar() != '\n');
}

// 自动存档函数
void AUTO_SAVE(int currentChapter, const char* lastText) {
    if (!g_auto_save_enabled) {
        return;
    }
    
    if (currentChapter == g_last_auto_save_chapter) {
        return;
    }
    
    int slot = g_auto_save_slot;
    
    if (saves[slot].chapter > 0) {
        char auto_save_marker[] = "[自动存档]";
        if (strstr(saves[slot].preview, auto_save_marker) == NULL) {
            printf("\n[自动存档] 警告：自动存档位%d已被手动存档占用！\n", slot+1);
            printf("第%d章 - %s\n", saves[slot].chapter, saves[slot].preview);
            printf("是否覆盖此手动存档？(y/n): ");
            
            char response = getchar();
            while(getchar() != '\n');
            
            if (response != 'y' && response != 'Y') {
                printf("[自动存档] 用户选择不覆盖，跳过自动存档\n");
                return;
            }
            printf("[自动存档] 覆盖手动存档...\n");
        } else {
            printf("\n[自动存档] 更新自动存档...\n");
        }
    }
    
    saves[slot].chapter = currentChapter;
    saves[slot].strange = g_strange;
    saves[slot].attention = g_attention;
    saves[slot].text_speed = g_text_speed;
    saves[slot].display_mode = g_display_mode;
    
    time_t now = time(NULL);
    struct tm* timeinfo = localtime(&now);
    strftime(saves[slot].saveTime, 20, "%Y-%m-%d %H:%M", timeinfo);
    
    char marked_preview[100];
    snprintf(marked_preview, sizeof(marked_preview), "[自动存档] %.80s", 
             strlen(lastText) > 0 ? lastText : "游戏进度");
    strncpy(saves[slot].preview, marked_preview, 99);
    saves[slot].preview[99] = '\0';
    
    char filename[20];
    sprintf(filename, "save%d.dat", slot+1);
    FILE* file = fopen(filename, "wb");
    if(file) {
        fwrite(&saves[slot], sizeof(struct SaveData), 1, file);
        fclose(file);
        printf("[自动存档] 游戏已自动存档到 存档位%d！\n", slot+1);
        g_last_auto_save_chapter = currentChapter;
    } else {
        printf("[自动存档] 自动存档失败！\n");
    }
}

// 设置文本颜色函数
void set_text_color(int color) {
    HANDLE hConsole = GetStdHandle(STD_OUTPUT_HANDLE);
    SetConsoleTextAttribute(hConsole, color);
}

// 屏幕闪烁函数
void flash_screen(int times) {
    HANDLE hConsole = GetStdHandle(STD_OUTPUT_HANDLE);
    CONSOLE_SCREEN_BUFFER_INFO csbi;
    GetConsoleScreenBufferInfo(hConsole, &csbi);
    WORD originalColor = csbi.wAttributes;
    
    printf("\n");
    
    for(int i = 0; i < times; i++) {
        SetConsoleTextAttribute(hConsole, 
            BACKGROUND_RED | BACKGROUND_INTENSITY | FOREGROUND_INTENSITY);
        printf("你是我的！");
        Sleep(150);
        
        SetConsoleTextAttribute(hConsole, originalColor);
        printf("\r                   \r");
        Sleep(150);
    }
    
    SetConsoleTextAttribute(hConsole, originalColor);
}

// 选择函数
int SELECT(struct Choice* choice){
    printf("\n%s\n",choice->prompt);

    for(int i=0;i<choice->optioncount;i++){
        printf("%d...%s\n",i+1,choice->option[i]);
    }

    int playerchoice;
    do
    {   printf("请选择(1-%d)：",choice->optioncount);
        if(scanf("%d",&playerchoice)!=1){
            while (getchar()!='\n'){}
            playerchoice=0;
        }
    } while (playerchoice<1||playerchoice>choice->optioncount);
    while (getchar()!='\n'){}
    return playerchoice-1;
}

// 慢速打印函数
void SP(const char* text, int base_sleeptime_ms){
    int actual_sleeptime = base_sleeptime_ms;
    
    if (g_text_speed >= 0) {
        actual_sleeptime = g_text_speed;
    }
    
    switch(g_display_mode) {
        case 0:
            for(int i = 0; text[i] != '\0'; i++) {
                putchar(text[i]);
                fflush(stdout);
                Sleep(actual_sleeptime);
            }
            break;
            
        case 1:
            printf("%s", text);
            fflush(stdout);
            break;
    }
    
    printf("\n");
}

// 文本设置菜单
void TEXT_SETTINGS_MENU() {
    int choice;
    do {
        printf("\n======= 设置 =======\n");
        if (g_text_speed == -1) {
            printf("当前速度: 使用剧本默认速度\n");
        } else {
            printf("当前速度: %d毫秒/字符\n", g_text_speed);
        }
        printf("当前模式: %s\n", g_display_mode == 0 ? "逐字显示" : "立即显示");
        printf("\n1. 调整文字速度\n");
        printf("2. 逐字显示/立即显示\n");
        printf("3. 自动存档设置\n");
        printf("4. 恢复默认设置\n");
        printf("5. 返回\n");
        printf("请选择: ");
        
        if(scanf("%d", &choice) != 1) {
            while(getchar() != '\n');
            choice = 0;
            continue;
        }
        while(getchar() != '\n');
        
        switch(choice) {
            case 1:
                {
                    int new_speed;
                    printf("请输入文字速度 (1-100毫秒，推荐10，输入-1使用剧本默认速度): ");
                    if(scanf("%d", &new_speed) == 1) {
                        if(new_speed >= 1 && new_speed <= 100) {
                            g_text_speed = new_speed;
                            printf("✓ 文字速度已设置为 %d 毫秒/字符\n", g_text_speed);
                        } else if(new_speed == -1) {
                            g_text_speed = -1;
                            printf("✓ 已设置为使用剧本默认速度\n");
                        } else {
                            printf("✗ 无效的速度值！请输入1-100或-1\n");
                        }
                    } else {
                        printf("✗ 输入错误！\n");
                    }
                    while(getchar() != '\n');
                }
                break;
                
            case 2:
                g_display_mode = (g_display_mode + 1) % 2;
                printf("✓ 显示模式已切换为: %s\n", 
                       g_display_mode == 0 ? "逐字显示" : "立即显示");
                break;
                
            case 3:
                {
                    printf("\n======= 自动存档设置 =======\n");
                    printf("当前状态: %s\n", g_auto_save_enabled ? "开启" : "关闭");
                    printf("自动存档位: %d\n", g_auto_save_slot + 1);
                    
                    if (saves[g_auto_save_slot].chapter > 0) {
                        char auto_save_marker[] = "[自动存档]";
                        char* is_auto_save = strstr(saves[g_auto_save_slot].preview, auto_save_marker);
                        
                        printf("当前存档: 第%d章 - %s %s\n", 
                               saves[g_auto_save_slot].chapter, 
                               saves[g_auto_save_slot].saveTime,
                               is_auto_save ? "(自动存档)" : "(手动存档-受保护)");
                    } else {
                        printf("当前存档: [空]\n");
                    }
                    
                    printf("\n所有存档位状态:\n");
                    for(int i = 0; i < MAX_SAVES; i++) {
                        if(saves[i].chapter == 0) {
                            printf("  存档位%d: [空]\n", i+1);
                        } else {
                            char auto_save_marker[] = "[自动存档]";
                            char* is_auto_save = strstr(saves[i].preview, auto_save_marker);
                            
                            printf("  存档位%d: 第%d章 %s\n", 
                                   i+1, saves[i].chapter,
                                   is_auto_save ? "(自动存档)" : "(手动存档)");
                        }
                    }
                    
                    printf("\n1. %s自动存档\n", g_auto_save_enabled ? "关闭" : "开启");
                    printf("2. 更改自动存档位\n");
                    printf("3. 立即创建自动存档\n");
                    printf("4. 查看自动存档内容\n");
                    printf("5. 返回\n");
                    printf("请选择: ");
                    
                    int auto_save_choice;
                    if(scanf("%d", &auto_save_choice) == 1) {
                        while(getchar() != '\n');
                        switch(auto_save_choice) {
                            case 1:
                                g_auto_save_enabled = !g_auto_save_enabled;
                                printf("✓ 自动存档已%s\n", g_auto_save_enabled ? "开启" : "关闭");
                                break;
                            case 2:
                                {
                                    int new_slot;
                                    printf("请输入自动存档位 (1-%d): ", MAX_SAVES);
                                    if(scanf("%d", &new_slot) == 1 && new_slot >= 1 && new_slot <= MAX_SAVES) {
                                        if (saves[new_slot-1].chapter > 0) {
                                            char auto_save_marker[] = "[自动存档]";
                                            char* is_auto_save = strstr(saves[new_slot-1].preview, auto_save_marker);
                                            
                                            if (is_auto_save == NULL) {
                                                printf("✗ 存档位%d已有手动存档，无法设置为自动存档位！\n", new_slot);
                                                break;
                                            }
                                        }
                                        
                                        g_auto_save_slot = new_slot - 1;
                                        printf("✓ 自动存档位已设置为 %d\n", new_slot);
                                    } else {
                                        printf("✗ 无效的存档位！\n");
                                    }
                                    while(getchar() != '\n');
                                }
                                break;
                            case 3:
                                AUTO_SAVE(g_last_auto_save_chapter > 0 ? g_last_auto_save_chapter : 1, "手动触发");
                                break;
                            case 4:
                                if (saves[g_auto_save_slot].chapter > 0) {
                                    printf("\n自动存档详情：\n");
                                    printf("存档位: %d\n", g_auto_save_slot + 1);
                                    printf("章节: 第%d章\n", saves[g_auto_save_slot].chapter);
                                    printf("时间: %s\n", saves[g_auto_save_slot].saveTime);
                                    printf("预览: %s\n", saves[g_auto_save_slot].preview);
                                    printf("特殊标记: strange=%d, attention=%d\n", 
                                           saves[g_auto_save_slot].strange, 
                                           saves[g_auto_save_slot].attention);
                                } else {
                                    printf("自动存档位为空\n");
                                }
                                break;
                        }
                    } else {
                        printf("✗ 输入错误！\n");
                        while(getchar() != '\n');
                    }
                }
                break;
            case 4:
                g_text_speed = 10;
                g_display_mode = 0;
                printf("✓ 已恢复默认设置（逐字显示，10毫秒/字符）\n");
                break;
                
            case 5:
                printf("返回主菜单...\n");
                break;
                
            default:
                printf("✗ 无效选择！请重新输入。\n");
                break;
        }
        
        if (choice >= 1 && choice <= 4) {
            printf("按回车键继续...");
            while(getchar() != '\n');
        }
        
    } while(choice != 5);
}

// 暂停菜单函数
void PAUSE_MENU(int currentChapter, const char* lastText) {
    int choice;
    do {
        printf("\n======= 暂停菜单 =======\n");
        printf("当前章节: 第%d章\n", currentChapter);
        if (g_text_speed == -1) {
            printf("当前速度: 使用剧本默认速度\n");
        } else {
            printf("当前速度: %d毫秒/字符\n", g_text_speed);
        }
        printf("当前模式: %s\n", g_display_mode == 0 ? "逐字显示" : "立即显示");
        printf("\n1. 继续游戏\n");
        printf("2. 设置\n");
        printf("3. 保存游戏\n");
        printf("4. 返回主菜单\n");
        printf("请选择: ");
        
        if(scanf("%d", &choice) != 1) {
            while(getchar() != '\n');
            choice = 0;
            continue;
        }
        while(getchar() != '\n');
        
        switch(choice) {
            case 1:
                printf("继续游戏...\n");
                break;
            case 2:
                TEXT_SETTINGS_MENU();
                break;
            case 3:
                SAVE_GAME(currentChapter, lastText);
                break;
            case 4:
                printf("返回主菜单...\n");
                g_return_to_menu = 1;
                break;
            default:
                printf("无效选择！\n");
                break;
        }
    } while(choice != 1 && choice != 4);
}

// 故事播放函数
void STORY(const char* filename, int startchapter) {
    int currentchapter = startchapter;
    int max_iterations = 1000;
    int iteration_count = 0;
    
    g_return_to_menu = 0;
    
    while(currentchapter > 0 && iteration_count < max_iterations && !g_return_to_menu) {
        iteration_count++;
        
        FILE* file = fopen(filename, "r");
        if(!file) {
            printf("错误！无法打开文件");
            return;
        }

        printf("\n第%d章\n", currentchapter);

        char line[1500];
        struct Choice currentchoice;
        int foundcurrentchapter = 0;
        int inchoice = 0;
        char lastDisplayedText[256] = "";
        int isFirstLine = 1;
        int nextchapter = 0;
        
        printf("按回车键开始本章节...\n");
        AUTO_SAVE(currentchapter, "已自动创建存档");
        int initial_input = getchar();
        while(initial_input != '\n' && initial_input != EOF) { 
            initial_input = getchar(); 
        }

        while(fgets(line, sizeof(line), file) && !g_return_to_menu) {
            line[strcspn(line, "\n")] = 0;
            if (line[0]=='#'||line[0]=='\0') {
                continue;
            }

            int chapter;
            char character[50], text[1500];
            if(sscanf(line, "%d,%[^,],%[^\n]", &chapter, character, text) == 3) {
                if (foundcurrentchapter && chapter > currentchapter) {
                    break;
                }

                if (chapter == currentchapter) {
                    foundcurrentchapter = 1;

                    // 处理特效指令
                    if(strcmp(character, "effect") == 0) {
                        if(strncmp(text, "color ", 6) == 0) {
                            int color = atoi(text+6);
                            set_text_color(color);
                        }
                        else if(strncmp(text, "flash ", 6) == 0) {
                            int times = atoi(text+6);
                            flash_screen(times);
                        }
                        continue;
                    }
                    
                    // 处理成就指令 - 新增成就系统支持
                    else if(strcmp(character, "achievement") == 0) {
                        UPDATE_ACHIEVEMENT_CONDITION(text);
                        continue;
                    }
                    
                    if (strcmp(character, "choice") == 0) {
                        inchoice = 1;
                        strcpy(currentchoice.prompt, text);
                        currentchoice.optioncount = 0;
                    }
                    else if(strcmp(character, "option") == 0 && inchoice) {
                        char* arrow = strstr(text, "->");
                        if (arrow) {
                            *arrow = 0;
                            
                            strcpy(currentchoice.option[currentchoice.optioncount], text);
                            currentchoice.aimchapter[currentchoice.optioncount] = atoi(arrow+2);
                            currentchoice.optioncount++;
                        }
                    }
                    else if(strcmp(character, "jump") == 0) {
                        nextchapter = atoi(text);
                        AUTO_SAVE(nextchapter, "新章节");
                        break;
                    }
                    else {
                        if(inchoice && currentchoice.optioncount > 0) {
                            int selected_index = SELECT(&currentchoice);
                            int selected_chapter = currentchoice.aimchapter[selected_index];
                            
                            if(strcmp(currentchoice.option[selected_index], "鑾Ξ鍗") == 0) {
                                g_attention = -1;
                                g_strange++;
                                
                                if (g_strange == 3) {
                                    nextchapter = 999;
                                } else {
                                    nextchapter = selected_chapter;
                                }
                            } else {
                                nextchapter = selected_chapter;
                            }
                            AUTO_SAVE(currentchapter, lastDisplayedText);
                            break;
                        }
                        
                        if (!isFirstLine) {
                            printf("\n");
                        }
                        isFirstLine = 0;
                        
                        printf("[%s]:", character);
                        SP(text, 10);
                        
                        strncpy(lastDisplayedText, text, 255);
                        lastDisplayedText[255] = '\0';
                        
                        printf("          Enter继续，输入s存档，p暂停：");
                        int c = getchar();
                        
                        if (c == 'S' || c == 's') {
                            SAVE_GAME(currentchapter, lastDisplayedText);
                            printf("          Enter继续，输入s存档，p暂停：");
                            c = getchar();
                            while(c != '\n' && c != EOF) { c = getchar(); }
                        } else if (c == 'P' || c == 'p') {
                            PAUSE_MENU(currentchapter, lastDisplayedText);
                            if (g_return_to_menu) {
                                fclose(file);
                                return;
                            }
                            printf("\n继续游戏...\n");
                        } else {
                            while(c != '\n' && c != EOF) { c = getchar(); }
                        }
                    }
                }
            } else {
                printf("解析失败！原文内容：%s\n", line);
            }
        }
        fclose(file);
        
        if (g_return_to_menu) {
            break;
        }
        
        if(nextchapter > 0) {
            currentchapter = nextchapter;
        } else if(!foundcurrentchapter) {
            printf("再也不会有下一章了……\n");
            break;
        } else {
            printf("本章结束。\n");
            break;
        }
    }
    
    if(iteration_count >= max_iterations) {
        printf("警告：可能陷入无限循环！\n");
    }
}

void SHOW_WELCOME() {
    char start[]="开始游戏前，请您务必认真阅读READMEPLEASE.txt。您应当事先了解，此游戏含有一定的暴力和Meta元素，您应当对此做好心理准备。如果您同意为自己的心理健康负责，按回车键开始游戏。您仍然可以随时退出游戏。";
    SP(start,1);
    int cc=getchar();
    while(cc!='\n'){}
}

int main(){
    SetConsoleOutputCP(65001);
    
    // 初始化成就系统
    INIT_ACHIEVEMENTS();
    
    // 加载所有存档
    LOAD_ALL_SAVES();
    
    // 主菜单循环
    int menuChoice;
    do {
        printf("\n======= Doki Doki Ohayou Sayori! =======\n");
        printf("1. 开始新游戏\n");
        printf("2. 读取存档\n");
        printf("3. 设置\n");
        printf("4. 成就系统\n");  // 新增成就系统选项
        printf("5. 退出游戏\n");
        printf("请选择: ");
        
        if(scanf("%d", &menuChoice) != 1) {
            while(getchar() != '\n');
            menuChoice = 0;
            continue;
        }
        while(getchar() != '\n');
        
        switch(menuChoice) {
            case 1:
                g_strange = 0;
                g_attention = 0;
                g_return_to_menu = 0;
                SHOW_WELCOME();
                STORY("story.txt", 1);
                break;
            case 2:
                {
                    int saveIndex = LOAD_GAME_MENU();
                    if(saveIndex >= 0) {
                        g_strange = saves[saveIndex].strange;
                        g_attention = saves[saveIndex].attention;
                        g_text_speed = saves[saveIndex].text_speed;
                        g_display_mode = saves[saveIndex].display_mode;
                        g_return_to_menu = 0;
                        printf("从存档继续游戏...\n");
                        printf("文本设置: %s, %s\n", 
                               g_text_speed == -1 ? "剧本默认速度" : "自定义速度",
                               g_display_mode == 0 ? "逐字显示" : "立即显示");
                        STORY("story.txt", saves[saveIndex].chapter);
                    }
                }
                break;
            case 3:
                TEXT_SETTINGS_MENU();
                break;
            case 4:  // 新增：成就系统
                ACHIEVEMENT_MENU();
                break;
            case 5:
                printf("拜拜！\n");
                break;
            default:
                printf("无效选择！请重新输入。\n");
        }
    } while(menuChoice != 5);
    
    return 0;
}