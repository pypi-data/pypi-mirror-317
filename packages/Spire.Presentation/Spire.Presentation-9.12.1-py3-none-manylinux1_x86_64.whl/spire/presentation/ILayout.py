from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.presentation.common import *
from spire.presentation import *
from ctypes import *
import abc

class ILayout (ActiveSlide) :
    """

    """
    @property

    def LayoutType(self)->'SlideLayoutType':
        """
    <summary>
        Gets layout type of this layout slide.
    </summary>
        """
        GetDllLibPpt().ILayout_get_LayoutType.argtypes=[c_void_p]
        GetDllLibPpt().ILayout_get_LayoutType.restype=c_int
        ret = CallCFunction(GetDllLibPpt().ILayout_get_LayoutType,self.Ptr)
        objwraped = SlideLayoutType(ret)
        return objwraped

#
#    def GetDependingSlides(self)->List['ISlide']:
#        """
#    <summary>
#         Gets an array with all slides, which depend on this layout slide.
#    </summary>
#        """
#        GetDllLibPpt().ILayout_GetDependingSlides.argtypes=[c_void_p]
#        GetDllLibPpt().ILayout_GetDependingSlides.restype=IntPtrArray
#        intPtrArray = CallCFunction(GetDllLibPpt().ILayout_GetDependingSlides,self.Ptr)
#        ret = GetVectorFromArray(intPtrArray, ISlide)
#        return ret


    @property

    def Name(self)->str:
        """
    <summary>
        Gets the name of the layout.
    </summary>
        """
        GetDllLibPpt().ILayout_get_Name.argtypes=[c_void_p]
        GetDllLibPpt().ILayout_get_Name.restype=c_void_p
        ret = PtrToStr(CallCFunction(GetDllLibPpt().ILayout_get_Name,self.Ptr))
        return ret


    @property
    def Shapes(self)->'ShapeCollection':
        """
    <summary>
        Gets the shapes of a slide.
            Read-only <see cref="T:Spire.Presentation.ShapeCollection" />.
    </summary>
        """
        GetDllLibPpt().ActiveSlide_get_Shapes.argtypes=[c_void_p]
        GetDllLibPpt().ActiveSlide_get_Shapes.restype=c_void_p
        intPtr = CallCFunction(GetDllLibPpt().ActiveSlide_get_Shapes,self.Ptr)
        ret = None if intPtr==None else ShapeCollection(intPtr)
        return ret
