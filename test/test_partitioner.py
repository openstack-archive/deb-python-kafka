import pytest
import six

from kafka.partitioner import Murmur2Partitioner
from kafka.partitioner.default import DefaultPartitioner
from kafka.partitioner.hashed import murmur2


def test_default_partitioner():
    partitioner = DefaultPartitioner()
    all_partitions = list(range(100))
    available = all_partitions
    # partitioner should return the same partition for the same key
    p1 = partitioner(b'foo', all_partitions, available)
    p2 = partitioner(b'foo', all_partitions, available)
    assert p1 == p2
    assert p1 in all_partitions

    # when key is None, choose one of available partitions
    assert partitioner(None, all_partitions, [123]) == 123

    # with fallback to all_partitions
    assert partitioner(None, all_partitions, []) in all_partitions


def test_murmur2_java_compatibility():
    p = Murmur2Partitioner(range(1000))
    # compare with output from Kafka's org.apache.kafka.clients.producer.Partitioner
    assert p.partition(b'') == 681
    assert p.partition(b'a') == 524
    assert p.partition(b'ab') == 434
    assert p.partition(b'abc') == 107
    assert p.partition(b'123456789') == 566
    assert p.partition(b'\x00 ') == 742


def test_murmur2_not_ascii():
    # Verify no regression of murmur2() bug encoding py2 bytes that dont ascii encode
    murmur2(b'\xa4')
    murmur2(b'\x81' * 1000)
