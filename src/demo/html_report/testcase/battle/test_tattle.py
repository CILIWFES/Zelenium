#! /usr/bin/env python
# -*- coding: UTF-8 -*-

from src.code import *


class TestBattle(unittest.TestCase):
    def test_start_battle(self):
        """测试开始战斗

        :return:
        """
        print("测试开始战斗")

    def test_skill_buff(self):
        """测试技能buff

        :return:
        """
        print("测试技能buff")

    @TestTag.tag(TestTag.Param.TEST)
    def test_normal_attack(self):
        """测试普通攻击

        :return:
        """
        print("TEST任务测试普通攻击")

    @TestTag.data({"gold": 1000, "diamond": 100}, {"gold": 2000, "diamond": 200}, unpack=False)
    def test_get_battle_reward(self, reward):
        """ 测试领取战斗奖励

        :return:
        """
        print(reward)
        print("测试领取战斗奖励，获得的钻石数量是：{}".format(reward['diamond']))
        scheduler.show_console("测试领取战斗奖励，获得的钻石数量是：{}".format(reward['diamond']), "I")
