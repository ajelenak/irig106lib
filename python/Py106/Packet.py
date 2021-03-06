'''
IRIG 106 Data DLL - This module provides an interface to the IRIG 106 data DLL.

The IRIG 106 DLL irig106.dll must be present somewhere in the system where
Windows can find it.

Message data structures are based on the ctypes module.  The main implication of
this is that to use data first the data buffer needs to be cast to the
appropriate data structure.  Then the fields are accessed using the '.contents'
attribute.

'''

import os.path
import sys
import platform
import ctypes
#import datetime
import Py106.Status as Status


# ---------------------------------------------------------------------------
# IRIG 106 data structures
# ---------------------------------------------------------------------------

class Header(ctypes.Structure):
    ''' Data structure for IRIG 106 packet primary and secondary header '''
    _pack_   = 1
    _fields_ = [("Sync",            ctypes.c_uint16),
                ("ChID",            ctypes.c_uint16),
                ("PacketLen",       ctypes.c_uint32),
                ("DataLen",         ctypes.c_uint32),
                ("HdrVer",          ctypes.c_uint8),
                ("SeqNum",          ctypes.c_uint8),
                ("PacketFlags",     ctypes.c_uint8),
                ("DataType",        ctypes.c_uint8),
                ("RefTime",         ctypes.c_uint8 * 6),
                ("Checksum",        ctypes.c_uint16),
                ("Time",            ctypes.c_uint32 * 2),
                ("Reserved",        ctypes.c_uint16),
                ("SecChecksum",     ctypes.c_uint16)]

# ---------------------------------------------------------------------------
# IRIG 106 constants
# ---------------------------------------------------------------------------


class FileMode():
    ''' Data file open mode '''
    CLOSED              = 0
    READ                = 1    # Open an existing file for reading
    OVERWRITE           = 2    # Create a new file or overwrite an exising file
    APPEND              = 3    # Append data to the end of an existing file
    READ_IN_ORDER       = 4    # Open an existing file for reading in time order
    READ_NET_STREAM     = 5    # Open network data stream


class DataType(object):
    ''' Packet Message Types '''
    COMPUTER_0          = 0x00
    USER_DEFINED        = 0x00
    COMPUTER_1          = 0x01
    TMATS               = 0x01
    COMPUTER_2          = 0x02
    RECORDING_EVENT     = 0x02
    COMPUTER_3          = 0x03
    RECORDING_INDEX     = 0x03
    COMPUTER_4          = 0x04
    COMPUTER_5          = 0x05
    COMPUTER_6          = 0x06
    COMPUTER_7          = 0x07
    PCM_FMT_0           = 0x08
    PCM_FMT_1           = 0x09
    IRIG_TIME           = 0x11
    MIL1553_FMT_1       = 0x19
    MIL1553_16PP194     = 0x1A      # 16PP194 Bus
    ANALOG              = 0x21
    DISCRETE            = 0x29
    MESSAGE             = 0x30
    ARINC_429_FMT_0     = 0x38
    VIDEO_FMT_0         = 0x40
    VIDEO_FMT_1         = 0x41
    VIDEO_FMT_2         = 0x42
    IMAGE_FMT_0         = 0x48
    IMAGE_FMT_1         = 0x49
    UART_FMT_0          = 0x50
    IEEE1394_FMT_0      = 0x58
    IEEE1394_FMT_1      = 0x59
    PARALLEL_FMT_0      = 0x60
    ETHERNET_FMT_0      = 0x68
    CAN_BUS             = 0x78
    FIBRE_CHAN_FMT_0    = 0x79
    FIBRE_CHAN_FMT_1    = 0x7A

    @staticmethod
    def TypeName(TypeNum):
        name = {DataType.USER_DEFINED       : "User Defined",
                DataType.TMATS              : "TMATS",
                DataType.RECORDING_EVENT    : "Event",
                DataType.RECORDING_INDEX    : "Index",
                DataType.COMPUTER_4         : "Computer Generated 4",
                DataType.COMPUTER_5         : "Computer Generated 5",
                DataType.COMPUTER_6         : "Computer Generated 6",
                DataType.COMPUTER_7         : "Computer Generated 7",
                DataType.PCM_FMT_0          : "PCM Format 0",
                DataType.PCM_FMT_1          : "PCM Format 1",
                DataType.IRIG_TIME          : "Time",
                DataType.MIL1553_FMT_1      : "1553",
                DataType.MIL1553_16PP194    : "16PP194",
                DataType.ANALOG             : "Analog",
                DataType.DISCRETE           : "Discrete",
                DataType.MESSAGE            : "Message",
                DataType.ARINC_429_FMT_0    : "ARINC 429",
                DataType.VIDEO_FMT_0        : "Video Format 0",
                DataType.VIDEO_FMT_1        : "Video Format 1",
                DataType.VIDEO_FMT_2        : "Video Format 2",
                DataType.IMAGE_FMT_0        : "Image Format 0",
                DataType.IMAGE_FMT_1        : "Image Format 1",
                DataType.UART_FMT_0         : "UART",
                DataType.IEEE1394_FMT_0     : "IEEE 1394 Format 0",
                DataType.IEEE1394_FMT_1     : "IEEE 1394 Format 1",
                DataType.PARALLEL_FMT_0     : "Parallel",
                DataType.ETHERNET_FMT_0     : "Ethernet",
                DataType.CAN_BUS            : "CAN Bus",
                DataType.FIBRE_CHAN_FMT_0   : "Fibre Channel Format 0",
                DataType.FIBRE_CHAN_FMT_1   : "Fibre Channel Format 1"}
        return name.get(TypeNum, "Undefined")


# ---------------------------------------------------------------------------
# Direct calls into the IRIG 106 dll
# ---------------------------------------------------------------------------

def I106_Ch10Open(file_name, file_mode):
    ''' Open IRIG 106 Ch 10 data file '''
    # file_name - File name to open
    # file_mode - Py106 FileMode() class value
    # Returns handle - IRIG file handle
    handle = ctypes.c_int32(0)
    # ret_status = IrigDataDll.enI106Ch10Open(ctypes.byref(handle), file_name,
    #                                         file_mode)
    ret_status = IrigDataDll.enI106Ch10Open(
        ctypes.byref(handle), file_name.encode('ascii'), file_mode)
    return (ret_status, handle)


def I106_Ch10Close(handle):
    ''' Close IRIG 106 Ch 10 data file '''
    # handle - IRIG file handle
    ret_status = IrigDataDll.enI106Ch10Close(handle)
    return ret_status


def I106_Ch10ReadNextHeader(handle, pkt_header):
    ''' Read next packet header '''
    # handle - IRIG file handle
    # pkt_header - Py106 Header() class, mutable
    ret_status = IrigDataDll.enI106Ch10ReadNextHeader(handle,
                                                      ctypes.byref(pkt_header))
    return ret_status


def I106_Ch10ReadPrevHeader(handle, pkt_header):
    ''' Read previous packet header '''
    # handle - IRIG file handle
    # pkt_header - Py106 class Header(), mutable
    ret_status = IrigDataDll.enI106Ch10ReadPrevHeader(handle,
                                                      ctypes.byref(pkt_header))
    return ret_status


def I106_Ch10ReadData(handle, buff_size, data_buff):
    # handle - IRIG file handle
    # buff_size - Size of data_buff
    # data_buff - Ctypes string buffer, mutable
    ret_status = IrigDataDll.enI106Ch10ReadData(handle, buff_size,
                                                ctypes.byref(data_buff))
    return ret_status


def I106_Ch10FirstMsg(handle):
    # handle - IRIG file handle
    ret_status = IrigDataDll.enI106Ch10FirstMsg(handle)
    return ret_status


def I106_Ch10LastMsg(handle):
    # handle - IRIG file handle
    ret_status = IrigDataDll.enI106Ch10LastMsg(handle)
    return ret_status


def I106_Ch10SetPos(handle, offset):
    # handle - IRIG file handle
    # offset - file offset
    ret_status = IrigDataDll.enI106Ch10SetPos(handle, offset)
    return ret_status


def I106_Ch10GetPos(handle):
    # handle - IRIG file handle
    offset = ctypes.c_uint64(0)
    ret_status = IrigDataDll.enI106Ch10GetPos(handle, ctypes.byref(offset))
    return (ret_status, offset.value)


# ---------------------------------------------------------------------------
# IRIG IO class
# ---------------------------------------------------------------------------

class IO(object):
    '''
    IRIG 106 packet data input / output
    '''

    # Constructor
    # -----------

    def __init__(self):
        self._Handle = ctypes.c_uint32(-1)
        self.Header = Header()
        self.Buffer = ctypes.create_string_buffer(0)

    # Open and close
    # --------------
    def open(self, Filename, FileMode):
        ''' Open an IRIG file for reading or writing '''
        RetStatus, self._Handle = I106_Ch10Open(Filename, FileMode)
        return RetStatus

    def close(self):
        ''' Close an open IRIG file '''
        RetStatus = I106_Ch10Close(self._Handle)
        return RetStatus

    # Read / Write
    # ------------
    def read_next_header(self):
        RetStatus = I106_Ch10ReadNextHeader(self._Handle, self.Header)
        return RetStatus

    def read_prev_header(self):
        RetStatus = I106_Ch10ReadPrevHeader(self._Handle, self.Header)
        return RetStatus

    def read_data(self):
        if self.Header.PacketLen > self.Buffer._length_:
            self.Buffer = ctypes.create_string_buffer(self.Header.PacketLen)
        RetStatus = I106_Ch10ReadData(self._Handle, self.Buffer._length_,
                                      self.Buffer)
        return RetStatus

    def packet_headers(self, ch_ids=()):
        ''' Iterator of individual packet headers '''
        RetStatus = self.read_next_header()
        while RetStatus == Status.OK:
            if (len(ch_ids) == 0) or (self.Header.ChID in ch_ids):
                yield self.Header
            RetStatus = self.read_next_header()

    # Other utility functions
    # -----------------------
    def first(self):
        ret_status = I106_Ch10FirstMsg(self._Handle)
        return ret_status

    def last(self):
        ret_status = I106_Ch10LastMsg(self._Handle)
        return ret_status

    def set_pos(self, offset):
        ret_status = I106_Ch10SetPos(self._Handle, offset)
        return ret_status

    def get_pos(self):
        (ret_status, offset) = I106_Ch10GetPos(self._Handle)
        return (ret_status, offset)


# ---------------------------------------------------------------------------
# Module initialization
# ---------------------------------------------------------------------------

# Load the correct dynamic library based on the platform
if platform.system() == "Windows":
    # 32 bit
    if (sys.maxsize < 2**32):
        DllFileName = "irig106.dll"
    # 64 bit
    else:
        DllFileName = "irig106-x64.dll"
else:
    DllFileName = "libirig106.so"

FilePath, FileName = os.path.split(__file__)
FullDllFileName = os.path.join(FilePath, DllFileName)
#print ("File               %s\n" % (__file__))
#print ("File Path          %s\n" % (FilePath))
#print ("Full DLL File Name %s\n" % (FullDllFileName))
#IrigDataDll = ctypes.cdll.LoadLibrary(DllFileName)
IrigDataDll = ctypes.cdll.LoadLibrary(FullDllFileName)

# This test code just opens an IRIG file and does a histogram of the
# data types

if __name__ == '__main__':

    print("IRIG 106 PacketIO")
    PktIO = IO()

    # Initialize counts variables
    Counts = {}

    if len(sys.argv) > 1:
        RetStatus = PktIO.open(sys.argv[1], FileMode.READ)
        if RetStatus != Status.OK:
            print("Error opening data file '%s'" % (sys.argv[1]))
            sys.exit(1)
    else:
        print("Usage : Packet.py <filename>")
        sys.exit(1)

#    The old traditional (aka FORTRAN) way of doing it
#    while True:
#        RetStatus = PktIO.read_next_header()
#        if RetStatus != Status.OK:
#            break
#        if Counts.has_key(PktIO.Header.DataType):
#           Counts[PktIO.Header.DataType] += 1
#        else:
#            Counts[PktIO.Header.DataType]  = 1

    # Using Python iteration
    for PktHdr in PktIO.packet_headers():
#        if Counts.has_key(PktHdr.DataType):
        if PktHdr.DataType in Counts:
            Counts[PktHdr.DataType] += 1
        else:
            Counts[PktHdr.DataType] = 1

    PktIO.close()

    for DataTypeNum in Counts:
        print("Data Type %-24s Counts = %d" % (DataType.TypeName(DataTypeNum),
                                               Counts[DataTypeNum]))
