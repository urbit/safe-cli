#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Import
from core.artifacts.help_artifacts import InformationArtifacts
from core.input.console_input_getter import ConsoleInputGetter
from eth_account import Account
from hexbytes import HexBytes

local_account0 = Account().privateKeyToAccount('0x4f3edf983ac636a65a842ce7c78d9aa706d3b113bce9c46f30d7d21715b23b1d')
local_account1 = Account().privateKeyToAccount('0x6cbed15c793ce57650b9877cf6fa156fbef513c4e6134f022a85b1ffdd59b2a1')
local_account2 = Account().privateKeyToAccount('0x6370fd033278c143179d81c5526140625662b8daa446c22ee2d73db3707e620c')
local_account3 = Account().privateKeyToAccount('0x646f1ce2fdad0e6deeeb5c7e8e5543bdde65e86029e2fd9fc169899c440a7913')
local_account4 = Account().privateKeyToAccount('0xadd53f9a7e588d003326d1cbf9e4a43c061aadd9bc938c843a79e7b4fd2ad743')
local_account5 = Account().privateKeyToAccount('0x395df67f0c2d2d9fe1ad08d1bc8b6627011959b79c53d7dd6a3536a33ab8a4fd')
local_account6 = Account().privateKeyToAccount('0xe485d098507f54e7733a205420dfddbe58db035fa577fc294ebd14db90767a52')
local_account7 = Account().privateKeyToAccount('0xa453611d9419d0e56f499079478fd72c37b251a94bfde4d19872c44cf65386e3')
local_account8 = Account().privateKeyToAccount('0x829e924fdf021ba3dbbc4225edfece9aca04b929d6e75613329ca6f1d31c0bb4')
local_account9 = Account().privateKeyToAccount('0xb0057716d5917badaf911b193b12b910811c1497b5bada8d7711f758981c3773')
new_account = local_account9

owners_list0 = [local_account0, local_account1, local_account2]
owners_list = [local_account4, local_account5, local_account6, local_account7, local_account8]


class ConsoleController:
    def __init__(self, logger, network_agent, console_accounts, console_payloads, console_tokens, contract_artifacts, console_engine):
        self.logger = logger

        # Assets
        self.contract_artifacts = contract_artifacts
        self.account_artifacts = console_accounts
        self.payload_artifacts = console_payloads
        self.token_artifacts = console_tokens
        self.network_agent = network_agent
        self.console_information = InformationArtifacts()

        self.console_engine = console_engine
        self.safe_interface = None
        self.contract_interface = None
        self.console_getter = ConsoleInputGetter(self.logger)

    def operate_with_console(self, desired_parsed_item_list, priority_group, command_argument, argument_list):
        """ Operate With Console
        This function will operate with the gnosis console using the input command/arguments provided by the user
        :param desired_parsed_item_list:
        :param priority_group:
        :param command_argument:
        :param argument_list:
        :param console_session:
        :return:
        """
        # load console console commands trigger procedures
        if command_argument == 'loadContract':
            self.contract_interface = self.console_engine.run_contract_console(desired_parsed_item_list, priority_group)
        elif command_argument == 'loadSafe':
            self.safe_interface = self.console_engine.run_safe_console(desired_parsed_item_list, priority_group)

        # view console commands procedures
        elif command_argument == 'viewNetwork':
            self.network_agent.command_view_networks()
        elif command_argument == 'viewContracts':
            self.contract_artifacts.command_view_contracts()
        elif command_argument == 'viewAccounts':
            self.account_artifacts.command_view_accounts()
        elif command_argument == 'viewPayloads':
            self.payload_artifacts.command_view_payloads()

        # new console commands trigger procedures
        elif command_argument == 'newAccount':
            # Add Ethereum money conversion for all types of coins
            self.logger.info('newAccount <Address> or <PK> or <PK + Address>')
        elif command_argument == 'newPayload':
            self.payload_artifacts.command_new_payload(command_argument, argument_list)
        elif command_argument == 'newTxPayload':
            self.payload_artifacts.command_new_payload(command_argument, argument_list)

        # setter console commands trigger procedures
        elif command_argument == 'setNetwork':
            self.network_agent.set_network_provider_endpoint('ganache', None)
        elif command_argument == 'setAutofill':
            print('Autofill Function')

        # test console getter commands trigger procedures
        elif command_argument == 'dummyCommand':
            #self.console_getter.get_gnosis_input_command_argument(stream)
            print('do nothing')
        # information console commands trigger procedures
        elif command_argument == 'about':
            self.console_information.command_view_about()
        elif (command_argument == 'info') or (command_argument == 'help'):
            self.console_information.command_view_help()

    def operate_with_safe(self, desired_parsed_item_list, priority_group, command_argument, argument_list, safe_interface):
        """ Operate With Safe
        This function will operate with the safe contract using the input command/arguments provided by the user
        :param desired_parsed_item_list:
        :param priority_group:
        :param command_argument:
        :param argument_list:
        :param safe_interface:
        :return:
        """
        self.logger.debug0('Operating with Safe: ' + command_argument)
        if command_argument == 'info':
            safe_interface.command_safe_information()
        elif command_argument == 'getOwners':
            safe_interface.command_safe_get_owners()
        elif command_argument == 'getThreshold':
            safe_interface.command_safe_get_threshold()
        elif command_argument == 'isOwner':
            # todo: Add priority group to the current getter
            if priority_group == 1:
                self.logger.debug0('desired parsed items' + str(desired_parsed_item_list))
                tmp_address = desired_parsed_item_list[0][1][0]
                self.logger.debug0('--address: {0}'.format(tmp_address))

            safe_interface.command_safe_is_owner(owners_list[0].address)
        elif command_argument == 'areOwners':
            safe_interface.command_safe_are_owners(owners_list)
        elif command_argument == 'nonce':
            safe_interface.command_safe_nonce()
        elif command_argument == 'code':
            safe_interface.command_safe_code()
        elif command_argument == 'VERSION':
            safe_interface.command_safe_version()
        elif command_argument == 'NAME':
            safe_interface.command_safe_name()
        elif command_argument == 'changeThreshold':
            if priority_group == 1:
                uint_value = desired_parsed_item_list[0][1][0]
                self.logger.debug0(uint_value)
                safe_interface.command_safe_change_threshold(int(uint_value), approval=False)

        elif command_argument == 'addOwnerWithThreshold':
            self.logger.debug0(desired_parsed_item_list)
            if priority_group == 1:
                address_value = ''
                uint_value = 0
                try:
                    address_value = desired_parsed_item_list[0][1][0]
                    uint_value = desired_parsed_item_list[1][1][0]
                    self.logger.info(str(address_value))
                    self.logger.info(str(uint_value))
                except Exception as err:
                    self.logger.info(err)
                safe_interface.command_safe_add_owner_threshold(str(address_value), int(uint_value), approval=False)

        elif command_argument == 'addOwner':
            self.logger.info(desired_parsed_item_list)
            if priority_group == 1:
                address_value = desired_parsed_item_list[0][1][0]
                self.logger.info(address_value)
                safe_interface.command_safe_add_owner_threshold(address_value, approval=False)

        elif command_argument == 'removeOwner':
            self.logger.debug0(desired_parsed_item_list)
            if priority_group == 1:
                address_value = ''
                previous_owner = ''
                try:
                    address_value = desired_parsed_item_list[0][1][0]
                    ordered_default_owner_list = sorted(safe_interface.default_owner_address_list, key=lambda v: v.lower())

                    self.logger.info('[ Current Owner with Address to be Removed ]: {0}'.format(str(address_value)))
                    self.logger.info('[ Finding Previous Owner ]: {0}'.format(safe_interface.default_owner_address_list))
                    self.logger.info('[ Ordered Default Addresses ]: {0}'.format(ordered_default_owner_list))

                    for index_owner, owner_address in enumerate(ordered_default_owner_list):
                        if owner_address == address_value:
                            self.logger.info('[ Found Owner on the list ]: {0}'.format(ordered_default_owner_list))
                            previous_owner = ordered_default_owner_list[index_owner - 1]
                            self.logger.info('[ Found PreviousOwner on the list ]: {0}'.format(previous_owner))
                            self.logger.info(previous_owner)

                except Exception as err:
                    self.logger.info(err)
                safe_interface.command_safe_remove_owner(str(previous_owner), str(address_value), approval=False)

        elif command_argument == 'removeMultipleOwners':

            safe_interface.command_safe_remove_owner(owners_list0[0], owners_list[1], approval=False)
        elif command_argument == 'swapOwner' or command_argument == 'changeOwner':
            self.logger.info(desired_parsed_item_list)
            if priority_group == 1:
                self.logger.info('')
            safe_interface.command_safe_swap_owner(owners_list0[0], owners_list0[1], new_account, approval=False)

        elif command_argument == 'sendToken':
            self.logger.info('sendToken to be Implemented')
        elif command_argument == 'sendEther':
            self.logger.info('sendEther to be Implemented')
            safe_interface.command_safe_send_ether(approval=False)
            # note: Eval --ether=, --miliether= sum(+) input
        elif command_argument == 'updateSafe':
            self.logger.info('updateSafe --address=0x to be Implemented')
            # note: Check Validity of The Safe Address & Version, Then Ask for Confirmation'

        elif command_argument == 'setDefaultSender':
            safe_interface.command_set_default_sender()
        elif command_argument == 'viewSender':
            safe_interface.command_view_default_sender()
            # view console commands procedures
        elif command_argument == 'viewNetwork':
            self.network_agent.command_view_networks()
        elif command_argument == 'viewContracts':
            self.contract_artifacts.command_view_contracts()
        elif command_argument == 'viewAccounts':
            self.account_artifacts.command_view_accounts()
        elif command_argument == 'viewPayloads':
            self.payload_artifacts.command_view_payloads()
        elif command_argument == 'loadOwner':
            if priority_group == 1:
                bytecode_value = desired_parsed_item_list[0][1][0]
                self.logger.debug0('[ Signature Value ]: {0} {1}'.format(str(bytecode_value), safe_interface.default_owner_address_list))
                local_owner = self.account_artifacts.get_local_account(bytecode_value, safe_interface.default_owner_address_list)
                safe_interface.local_owner_account_list.append(local_owner)

                self.logger.info('[ Local Account Added ]: {0}'.format(safe_interface.local_owner_account_list))
                self.logger.info('[ Data Output ]: {0} | {1} | {2}'.format(
                    local_owner, local_owner.address, HexBytes(local_owner.privateKey).hex())
                )
        elif command_argument == 'loadMultipleOwners':
            self.logger.info('load multiple owners')
        elif command_argument == 'unloadMultipleOwners':
            self.logger.info('load multiple owners')
        elif command_argument == 'unloadOwner':
            bytecode_value = desired_parsed_item_list[0][1][0]
            self.logger.debug0('[ Signature Value ]: {0} {1}'.format(str(bytecode_value), safe_interface.default_owner_address_list))
            local_owner = self.account_artifacts.get_local_account(bytecode_value, safe_interface.default_owner_address_list)
            for local_owner_account in safe_interface.local_owner_account_list:
                if local_owner_account == local_owner:
                    safe_interface.local_owner_account_list.remove(local_owner)
            self.logger.info('[ Local Account Subs ]: {0}'.format(safe_interface.local_owner_account_list))

    def operate_with_contract(self, stream, contract_methods, contract_instance):
        """ Operate With Contract
        This function will retrieve the methods present in the contract_instance
        :param stream: command_argument (method to call) that will trigger the operation
        :param contract_methods: dict with all the avaliable methods retrieved from the abi file
        :param contract_instance: only for eval() so it can be triggered
        :return: if method found, a method from the current contract will be triggered, success or
        not depends on the establishing of the proper values.
        """
        try:
            for item in contract_methods:
                if contract_methods[item]['name'] in stream:
                    splitted_stream = stream.split(' ')
                    function_name, function_arguments, address_from, execute_flag, queue_flag, query_flag = \
                        self.console_getter.get_input_method_arguments(splitted_stream, contract_methods[item]['arguments'])
                    self.logger.debug0('command: {0} | arguments: {1} | execute_flag: {2} | query_flag: {3} | '.format(function_name, function_arguments, execute_flag, queue_flag))

                    if execute_flag or query_flag or queue_flag:
                        # remark: Transaction Solver
                        if execute_flag:
                            if contract_methods[item]['name'].startswith('get'):
                                self.logger.warn('transact() operation is discourage if you are using a getter method')
                            # if address_from != '':
                                # address_from = '\{\'from\':{0}\}'.format(address_from)

                            self.logger.info(contract_methods[item]['transact'].format(function_arguments, address_from))
                            resolution = eval(contract_methods[item]['transact'].format(function_arguments, address_from))
                            self.logger.info(resolution)
                            # this is the hash to be signed, maybe call for approve dialog, approveHash dialogue,
                            # map functions to be performed by the gnosis_py library

                        # remark: Call Solver
                        elif query_flag:
                            self.logger.info(contract_methods[item]['call'].format(function_arguments, address_from))
                            resolution = eval(contract_methods[item]['call'].format(function_arguments, address_from))
                            self.logger.info(resolution)
                        # remark: Add to the Batch Solver
                        elif queue_flag:
                            self.logger.info('(Future Implementation) executeBatch when you are ready to launch the transactions that you queued up!')
                    else:
                        self.logger.warn('--execute, --query or --queue arguments needed in order to properly operate with the current contract')

        except Exception as err:
            self.logger.debug0('operate_with_contract() {0}'.format(err))