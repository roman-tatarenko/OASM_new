from datetime import datetime

import pytest
from pytest_testrail.plugin import pytestrail


@pytestrail.case('C7951')
def test_on_successfully_sending_a_contract_for_verification_full_payload(producer, consumer,
                                                                          prepared_cpid, prepared_ev_for_registration,
                                                                          prepared_ac_ocid,
                                                                          prepared_ac_for_registration,
                                                                          prepared_ev_ocid, prepared_ac_id,
                                                                          prepared_ev_id, prepared_record,
                                                                          execute_insert_into_notice_compiled_release,
                                                                          clear_notice_compiled_release_by_cpid):
    execute_insert_into_notice_compiled_release(cp_id=prepared_cpid, oc_id=prepared_ev_ocid,
                                                json_data=prepared_ev_for_registration,
                                                publish_date=datetime.now(), release_date=datetime.now(),
                                                release_id=prepared_ev_id,
                                                stage='EV', status='active')

    execute_insert_into_notice_compiled_release(cp_id=prepared_cpid, oc_id=prepared_ac_ocid,
                                                json_data=prepared_ac_for_registration,
                                                publish_date=datetime.now(), release_date=datetime.now(),
                                                release_id=prepared_ac_id,
                                                stage='AC', status='active')

    producer.send(topic='mconnect-bus-in', value=prepared_record)

    consumer.subscribe(['mconnect-bus-out'])

    data = None
    for message in consumer:
        message = message.value.decode()
        if f'{prepared_ac_ocid}' in message:
            data = message
            break

    if data:
        assert prepared_ac_ocid in data
    else:
        pytest.xfail("Record not found in topic Kafka")


@pytestrail.case('C7957')
def test_the_Transport_Agent_behavior_if_it_hasnt_found_a_tender_record(producer, consumer,
                                                                        prepared_cpid, prepared_ev_for_registration,
                                                                        prepared_ac_for_registration,
                                                                        prepared_ac_ocid, prepared_ev_ocid,
                                                                        prepared_ac_id, prepared_ev_id,
                                                                        execute_insert_into_notice_compiled_release,
                                                                        prepared_record,
                                                                        clear_notice_compiled_release_by_cpid):
    execute_insert_into_notice_compiled_release(cp_id=prepared_cpid, oc_id=prepared_ev_ocid,
                                                json_data=prepared_ev_for_registration,
                                                publish_date=datetime.now(), release_date=datetime.now(),
                                                release_id=prepared_ev_id,
                                                stage='EV', status='active')

    prepared_ac_for_registration['relatedProcesses'][0]['identifier'] = 'invalid'

    execute_insert_into_notice_compiled_release(cp_id=prepared_cpid, oc_id=prepared_ac_ocid,
                                                json_data=prepared_ac_for_registration,
                                                publish_date=datetime.now(), release_date=datetime.now(),
                                                release_id=prepared_ac_id,
                                                stage='AC', status='active')

    producer.send(topic='mconnect-bus-in', value=prepared_record)

    consumer.subscribe(['incidents'])

    data = None
    for message in consumer:
        message = message.value.decode()
        if f'{prepared_ac_ocid}' in message:
            data = message
            break

    if data:
        assert "ER-3.11.2.8" in data
    else:
        pytest.xfail("Record not found in topic Kafka")


@pytestrail.case('C8183')
def test_the_Transport_Agent_behavior_if_budgetBreakdownID_from_AC_not_equal_to_budgetBreakdownID_from_mconnect_bus_in(
        producer, consumer,
        prepared_cpid,
        prepared_ac_ocid, prepared_ev_ocid, prepared_ev_for_registration, prepared_ac_for_registration,
        prepared_ac_id, prepared_ev_id,
        execute_insert_into_notice_compiled_release,
        prepared_record,
        clear_notice_compiled_release_by_cpid):
    execute_insert_into_notice_compiled_release(cp_id=prepared_cpid, oc_id=prepared_ev_ocid,
                                                json_data=prepared_ev_for_registration,
                                                publish_date=datetime.now(), release_date=datetime.now(),
                                                release_id=prepared_ev_id,
                                                stage='EV', status='active')

    prepared_ac_for_registration['planning']['budget']['budgetAllocation'][0]['budgetBreakdownID'] = 'invalid'

    execute_insert_into_notice_compiled_release(cp_id=prepared_cpid, oc_id=prepared_ac_ocid,
                                                json_data=prepared_ac_for_registration,
                                                publish_date=datetime.now(), release_date=datetime.now(),
                                                release_id=prepared_ac_id,
                                                stage='AC', status='active')

    producer.send(topic='mconnect-bus-in', value=prepared_record)

    consumer.subscribe(['incidents'])

    data = None
    for message in consumer:
        message = message.value.decode()
        if f'{prepared_ac_ocid}' in message:
            data = message
            break

    if data:
        assert "ER-3.11.2.9" in data
    else:
        pytest.xfail(f"Record {prepared_ac_ocid} not found in topic Kafka")


@pytestrail.case('C7980')
def test_the_Transport_Agent_behavior_if_it_cant_find_value_for_details_byear_in_the_contract_release(
        producer, consumer,
        prepared_cpid, prepared_ac_for_registration, prepared_ev_for_registration,
        prepared_ac_ocid, prepared_ev_ocid,
        prepared_ac_id, prepared_ev_id,
        execute_insert_into_notice_compiled_release,
        prepared_record,
        clear_notice_compiled_release_by_cpid):
    execute_insert_into_notice_compiled_release(cp_id=prepared_cpid, oc_id=prepared_ev_ocid,
                                                json_data=prepared_ev_for_registration,
                                                publish_date=datetime.now(), release_date=datetime.now(),
                                                release_id=prepared_ev_id,
                                                stage='EV', status='active')

    prepared_ac_for_registration['planning']['budget']['budgetAllocation'][0]['period']['startDate'] = None

    execute_insert_into_notice_compiled_release(cp_id=prepared_cpid, oc_id=prepared_ac_ocid,
                                                json_data=prepared_ac_for_registration,
                                                publish_date=datetime.now(), release_date=datetime.now(),
                                                release_id=prepared_ac_id,
                                                stage='AC', status='active')

    producer.send(topic='mconnect-bus-in', value=prepared_record)

    consumer.subscribe(['incidents'])

    data = None
    for message in consumer:
        message = message.value.decode()
        if f'{prepared_ac_ocid}' in message:
            data = message
            break

    if data:
        assert "ER-3.11.2.9" in data
    else:
        pytest.xfail(f"Record {prepared_ac_ocid} not found in topic Kafka")


@pytestrail.case('C7958')
def test_the_Transport_Agent_behavior_if_it_hasnt_found_a_contract_record(producer, consumer, prepared_ac_ocid,
                                                                          prepared_record):
    producer.send(topic='mconnect-bus-in', value=prepared_record)

    consumer.subscribe(['incidents'])

    data = None
    for message in consumer:
        message = message.value.decode()
        if f'{prepared_ac_ocid}' in message:
            data = message
            break

    if data:
        assert "ER-3.11.2.7" in data
    else:
        pytest.xfail(f"Record {prepared_ac_ocid} not found in topic Kafka")


@pytest.mark.skip
@pytestrail.case('7959')
def test_the_registered_contract_cant_be_sent_for_registration():
    pass


@pytestrail.case('8007')
def test_on_successfully_sending_a_contract_for_verification_payload_with_only_obligatory_attributes(
        execute_insert_into_notice_compiled_release, prepared_cpid, prepared_ev_ocid, prepared_ev_for_registration,
        prepared_ev_id, prepared_ac_ocid, prepared_ac_for_registration, prepared_ac_id):
    execute_insert_into_notice_compiled_release(cp_id=prepared_cpid, oc_id=prepared_ev_ocid,
                                                json_data=prepared_ev_for_registration,
                                                publish_date=datetime.now(), release_date=datetime.now(),
                                                release_id=prepared_ev_id,
                                                stage='EV', status='active')

    prepared_ac_for_registration['planning']['implementation']['transactions'][0]['type'] = "payment"

    parties = prepared_ac_for_registration['parties'].copy()

    for party in parties:
        if any(i in ("buyer", "supplier") for i in party['roles']):
            for additionalIdentifier in party['additionalIdentifiers']:
                if additionalIdentifier['scheme'] == 'MD-BRANCHES':
                    prepared_ac_for_registration.remove(party)

    execute_insert_into_notice_compiled_release(cp_id=prepared_cpid, oc_id=prepared_ac_ocid,
                                                json_data=prepared_ac_for_registration,
                                                publish_date=datetime.now(), release_date=datetime.now(),
                                                release_id=prepared_ac_id,
                                                stage='AC', status='active')
