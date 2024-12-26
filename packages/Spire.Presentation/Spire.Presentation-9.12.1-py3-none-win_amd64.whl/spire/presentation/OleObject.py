from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.presentation.common import *
from spire.presentation import *
from ctypes import *
import abc

class OleObject (  IActiveSlide, IActivePresentation) :
    """
    <summary>
        Represents an Ole object.
    </summary>
    """
    @property

    def Name(self)->str:
        """
    <summary>
        Gets the name of this control.
            Readonly <see cref="T:System.String" />.
    </summary>
        """
        GetDllLibPpt().OleObject_get_Name.argtypes=[c_void_p]
        GetDllLibPpt().OleObject_get_Name.restype=c_void_p
        ret = PtrToStr(CallCFunction(GetDllLibPpt().OleObject_get_Name,self.Ptr))
        return ret


    @property

    def PictureFill(self)->'PictureFillFormat':
        """
    <summary>
        Gets Control image fill properties object.
            Readonly <see cref="T:Spire.Presentation.Drawing.PictureFillFormat" />.
    </summary>
        """
        GetDllLibPpt().OleObject_get_PictureFill.argtypes=[c_void_p]
        GetDllLibPpt().OleObject_get_PictureFill.restype=c_void_p
        intPtr = CallCFunction(GetDllLibPpt().OleObject_get_PictureFill,self.Ptr)
        ret = None if intPtr==None else PictureFillFormat(intPtr)
        return ret


    @property

    def Frame(self)->'GraphicFrame':
        """
    <summary>
        Gets or sets control's frame.
            Read/write <see cref="F:Spire.Presentation.OleObject.GraphicFrame" />.
    </summary>
        """
        GetDllLibPpt().OleObject_get_Frame.argtypes=[c_void_p]
        GetDllLibPpt().OleObject_get_Frame.restype=c_void_p
        intPtr = CallCFunction(GetDllLibPpt().OleObject_get_Frame,self.Ptr)
        ret = None if intPtr==None else GraphicFrame(intPtr)
        return ret


    @Frame.setter
    def Frame(self, value:'GraphicFrame'):
        GetDllLibPpt().OleObject_set_Frame.argtypes=[c_void_p, c_void_p]
        CallCFunction(GetDllLibPpt().OleObject_set_Frame,self.Ptr, value.Ptr)

    @property

    def Properties(self)->'OleObjectProperties':
        """
    <summary>
        Gets a collection of OleObject properties.
            Readonly <see cref="T:Spire.Presentation.Collections.OleObjectProperties" />.
    </summary>
        """
        GetDllLibPpt().OleObject_get_Properties.argtypes=[c_void_p]
        GetDllLibPpt().OleObject_get_Properties.restype=c_void_p
        intPtr = CallCFunction(GetDllLibPpt().OleObject_get_Properties,self.Ptr)
        ret = None if intPtr==None else OleObjectProperties(intPtr)
        return ret


