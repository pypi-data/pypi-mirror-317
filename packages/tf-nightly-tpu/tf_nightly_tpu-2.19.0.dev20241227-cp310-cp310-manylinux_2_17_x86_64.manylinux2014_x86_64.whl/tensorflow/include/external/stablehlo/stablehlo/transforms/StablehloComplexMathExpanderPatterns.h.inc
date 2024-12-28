/*===- TableGen'erated file -------------------------------------*- C++ -*-===*\
|*                                                                            *|
|* Rewriters                                                                  *|
|*                                                                            *|
|* Automatically generated file, do not edit!                                 *|
|* From: StablehloComplexMathExpanderPatterns.td                              *|
|*                                                                            *|
\*===----------------------------------------------------------------------===*/


static ::llvm::LogicalResult __mlir_ods_local_type_constraint_StablehloComplexMathExpanderPatterns1(
    ::mlir::PatternRewriter &rewriter, ::mlir::Operation *op, ::mlir::Type type,
    ::llvm::StringRef failureStr) {
  if (!((isa<ComplexType>(cast<ShapedType>(type).getElementType())))) {
    return rewriter.notifyMatchFailure(op, [&](::mlir::Diagnostic &diag) {
      diag << failureStr << ": Complex element type";
    });
  }
  return ::mlir::success();
}
/* Generated from:
    external/stablehlo/stablehlo/transforms/StablehloComplexMathExpanderPatterns.td:142
*/
struct Log1pOp_ComplexElementType_ComplexMathExpander : public ::mlir::RewritePattern {
  Log1pOp_ComplexElementType_ComplexMathExpander(::mlir::MLIRContext *context)
      : ::mlir::RewritePattern("stablehlo.log_plus_one", 1, context, {"stablehlo.abs", "stablehlo.add", "stablehlo.atan2", "stablehlo.compare", "stablehlo.complex", "stablehlo.divide", "stablehlo.imag", "stablehlo.log", "stablehlo.log_plus_one", "stablehlo.maximum", "stablehlo.minimum", "stablehlo.multiply", "stablehlo.negate", "stablehlo.real", "stablehlo.select", "stablehlo.sqrt", "stablehlo.subtract"}) {}
  ::llvm::LogicalResult matchAndRewrite(::mlir::Operation *op0,
      ::mlir::PatternRewriter &rewriter) const override {
    // Variables for capturing values and attributes used while creating ops
    ::mlir::Operation::operand_range z(op0->getOperands());
    ::llvm::SmallVector<::mlir::Operation *, 4> tblgen_ops;

    // Match
    tblgen_ops.push_back(op0);
    auto castedOp0 = ::llvm::dyn_cast<::mlir::stablehlo::Log1pOp>(op0); (void)castedOp0;
    if(::mlir::failed(__mlir_ods_local_type_constraint_StablehloComplexMathExpanderPatterns1(rewriter, castedOp0, (*castedOp0.getODSOperands(0).begin()).getType(), "operand 0 of op 'stablehlo.log_plus_one' failed to satisfy constraint: 'Complex element type'"))) {
      return ::mlir::failure();
    }
    z = castedOp0.getODSOperands(0);

    // Rewrite
    auto odsLoc = rewriter.getFusedLoc({tblgen_ops[0]->getLoc()}); (void)odsLoc;
    ::llvm::SmallVector<::mlir::Value, 4> tblgen_repl_values;
    ::mlir::stablehlo::RealOp x;
    {
      ::mlir::Value tblgen_value_0 = (*z.begin());
      x = rewriter.create<::mlir::stablehlo::RealOp>(odsLoc,
        /*operand=*/tblgen_value_0
      );
    }
    ::mlir::stablehlo::AbsOp ax;
    {
      ::mlir::Value tblgen_value_0 = (*x.getODSResults(0).begin());
      ax = rewriter.create<::mlir::stablehlo::AbsOp>(odsLoc,
        /*operand=*/tblgen_value_0
      );
    }
    ::mlir::stablehlo::ImagOp y;
    {
      ::mlir::Value tblgen_value_0 = (*z.begin());
      y = rewriter.create<::mlir::stablehlo::ImagOp>(odsLoc,
        /*operand=*/tblgen_value_0
      );
    }
    ::mlir::stablehlo::AbsOp ay;
    {
      ::mlir::Value tblgen_value_0 = (*y.getODSResults(0).begin());
      ay = rewriter.create<::mlir::stablehlo::AbsOp>(odsLoc,
        /*operand=*/tblgen_value_0
      );
    }
    ::mlir::stablehlo::MaxOp mx;
    {
      ::mlir::Value tblgen_value_0 = (*ax.getODSResults(0).begin());
      ::mlir::Value tblgen_value_1 = (*ay.getODSResults(0).begin());
      mx = rewriter.create<::mlir::stablehlo::MaxOp>(odsLoc,
        /*lhs=*/tblgen_value_0,
        /*rhs=*/tblgen_value_1
      );
    }
    auto largest = ::mlir::stablehlo::getConstantLikeMaxFiniteValue(rewriter, odsLoc, (*x.getODSResults(0).begin())); (void)largest;
    ::mlir::stablehlo::SqrtOp tblgen_SqrtOp_0;
    {
      ::mlir::Value tblgen_value_0 = largest;
      tblgen_SqrtOp_0 = rewriter.create<::mlir::stablehlo::SqrtOp>(odsLoc,
        /*operand=*/tblgen_value_0
      );
    }
    auto nativeVar_1 = ::mlir::stablehlo::getConstantLike(rewriter, odsLoc, 0.01, (*x.getODSResults(0).begin())); (void)nativeVar_1;
    ::mlir::stablehlo::MulOp tblgen_MulOp_2;
    {
      ::mlir::Value tblgen_value_0 = (*tblgen_SqrtOp_0.getODSResults(0).begin());
      ::mlir::Value tblgen_value_1 = nativeVar_1;
      tblgen_MulOp_2 = rewriter.create<::mlir::stablehlo::MulOp>(odsLoc,
        /*lhs=*/tblgen_value_0,
        /*rhs=*/tblgen_value_1
      );
    }
    auto nativeVar_3 = ::mlir::stablehlo::ComparisonTypeAttr(); (void)nativeVar_3;
    ::mlir::stablehlo::CompareOp tblgen_CompareOp_4;
    {
      ::mlir::Value tblgen_value_0 = (*mx.getODSResults(0).begin());
      ::mlir::Value tblgen_value_1 = (*tblgen_MulOp_2.getODSResults(0).begin());
      tblgen_CompareOp_4 = rewriter.create<::mlir::stablehlo::CompareOp>(odsLoc,
        /*lhs=*/tblgen_value_0,
        /*rhs=*/tblgen_value_1,
        ::mlir::stablehlo::ComparisonDirectionAttr::get(rewriter.getContext(), ::mlir::stablehlo::ComparisonDirection::GT),
        /*compare_type=*/nativeVar_3
      );
    }
    ::mlir::stablehlo::LogOp tblgen_LogOp_5;
    {
      ::mlir::Value tblgen_value_0 = (*mx.getODSResults(0).begin());
      tblgen_LogOp_5 = rewriter.create<::mlir::stablehlo::LogOp>(odsLoc,
        /*operand=*/tblgen_value_0
      );
    }
    auto half = ::mlir::stablehlo::getConstantLike(rewriter, odsLoc, 0.5, (*x.getODSResults(0).begin())); (void)half;
    ::mlir::stablehlo::MinOp mn;
    {
      ::mlir::Value tblgen_value_0 = (*ax.getODSResults(0).begin());
      ::mlir::Value tblgen_value_1 = (*ay.getODSResults(0).begin());
      mn = rewriter.create<::mlir::stablehlo::MinOp>(odsLoc,
        /*lhs=*/tblgen_value_0,
        /*rhs=*/tblgen_value_1
      );
    }
    auto nativeVar_6 = ::mlir::stablehlo::ComparisonTypeAttr(); (void)nativeVar_6;
    ::mlir::stablehlo::CompareOp tblgen_CompareOp_7;
    {
      ::mlir::Value tblgen_value_0 = (*mn.getODSResults(0).begin());
      ::mlir::Value tblgen_value_1 = (*mx.getODSResults(0).begin());
      tblgen_CompareOp_7 = rewriter.create<::mlir::stablehlo::CompareOp>(odsLoc,
        /*lhs=*/tblgen_value_0,
        /*rhs=*/tblgen_value_1,
        ::mlir::stablehlo::ComparisonDirectionAttr::get(rewriter.getContext(), ::mlir::stablehlo::ComparisonDirection::EQ),
        /*compare_type=*/nativeVar_6
      );
    }
    auto one = ::mlir::stablehlo::getConstantLike(rewriter, odsLoc, 1, (*x.getODSResults(0).begin())); (void)one;
    ::mlir::stablehlo::DivOp r;
    {
      ::mlir::Value tblgen_value_0 = (*mn.getODSResults(0).begin());
      ::mlir::Value tblgen_value_1 = (*mx.getODSResults(0).begin());
      r = rewriter.create<::mlir::stablehlo::DivOp>(odsLoc,
        /*lhs=*/tblgen_value_0,
        /*rhs=*/tblgen_value_1
      );
    }
    ::mlir::stablehlo::MulOp tblgen_MulOp_8;
    {
      ::mlir::Value tblgen_value_0 = (*r.getODSResults(0).begin());
      ::mlir::Value tblgen_value_1 = (*r.getODSResults(0).begin());
      tblgen_MulOp_8 = rewriter.create<::mlir::stablehlo::MulOp>(odsLoc,
        /*lhs=*/tblgen_value_0,
        /*rhs=*/tblgen_value_1
      );
    }
    ::mlir::stablehlo::SelectOp tblgen_SelectOp_9;
    {
      ::mlir::Value tblgen_value_0 = (*tblgen_CompareOp_7.getODSResults(0).begin());
      ::mlir::Value tblgen_value_1 = one;
      ::mlir::Value tblgen_value_2 = (*tblgen_MulOp_8.getODSResults(0).begin());
      tblgen_SelectOp_9 = rewriter.create<::mlir::stablehlo::SelectOp>(odsLoc,
        /*pred=*/tblgen_value_0,
        /*on_true=*/tblgen_value_1,
        /*on_false=*/tblgen_value_2
      );
    }
    ::mlir::stablehlo::Log1pOp tblgen_Log1pOp_10;
    {
      ::mlir::Value tblgen_value_0 = (*tblgen_SelectOp_9.getODSResults(0).begin());
      tblgen_Log1pOp_10 = rewriter.create<::mlir::stablehlo::Log1pOp>(odsLoc,
        /*operand=*/tblgen_value_0
      );
    }
    ::mlir::stablehlo::MulOp tblgen_MulOp_11;
    {
      ::mlir::Value tblgen_value_0 = half;
      ::mlir::Value tblgen_value_1 = (*tblgen_Log1pOp_10.getODSResults(0).begin());
      tblgen_MulOp_11 = rewriter.create<::mlir::stablehlo::MulOp>(odsLoc,
        /*lhs=*/tblgen_value_0,
        /*rhs=*/tblgen_value_1
      );
    }
    ::mlir::stablehlo::AddOp tblgen_AddOp_12;
    {
      ::mlir::Value tblgen_value_0 = (*tblgen_LogOp_5.getODSResults(0).begin());
      ::mlir::Value tblgen_value_1 = (*tblgen_MulOp_11.getODSResults(0).begin());
      tblgen_AddOp_12 = rewriter.create<::mlir::stablehlo::AddOp>(odsLoc,
        /*lhs=*/tblgen_value_0,
        /*rhs=*/tblgen_value_1
      );
    }
    ::mlir::stablehlo::AddOp xp1;
    {
      ::mlir::Value tblgen_value_0 = (*x.getODSResults(0).begin());
      ::mlir::Value tblgen_value_1 = one;
      xp1 = rewriter.create<::mlir::stablehlo::AddOp>(odsLoc,
        /*lhs=*/tblgen_value_0,
        /*rhs=*/tblgen_value_1
      );
    }
    ::mlir::stablehlo::AbsOp tblgen_AbsOp_13;
    {
      ::mlir::Value tblgen_value_0 = (*xp1.getODSResults(0).begin());
      tblgen_AbsOp_13 = rewriter.create<::mlir::stablehlo::AbsOp>(odsLoc,
        /*operand=*/tblgen_value_0
      );
    }
    ::mlir::stablehlo::AddOp tblgen_AddOp_14;
    {
      ::mlir::Value tblgen_value_0 = (*tblgen_AbsOp_13.getODSResults(0).begin());
      ::mlir::Value tblgen_value_1 = (*ay.getODSResults(0).begin());
      tblgen_AddOp_14 = rewriter.create<::mlir::stablehlo::AddOp>(odsLoc,
        /*lhs=*/tblgen_value_0,
        /*rhs=*/tblgen_value_1
      );
    }
    auto nativeVar_15 = ::mlir::stablehlo::getConstantLike(rewriter, odsLoc, 0.2, (*x.getODSResults(0).begin())); (void)nativeVar_15;
    auto nativeVar_16 = ::mlir::stablehlo::ComparisonTypeAttr(); (void)nativeVar_16;
    ::mlir::stablehlo::CompareOp tblgen_CompareOp_17;
    {
      ::mlir::Value tblgen_value_0 = (*tblgen_AddOp_14.getODSResults(0).begin());
      ::mlir::Value tblgen_value_1 = nativeVar_15;
      tblgen_CompareOp_17 = rewriter.create<::mlir::stablehlo::CompareOp>(odsLoc,
        /*lhs=*/tblgen_value_0,
        /*rhs=*/tblgen_value_1,
        ::mlir::stablehlo::ComparisonDirectionAttr::get(rewriter.getContext(), ::mlir::stablehlo::ComparisonDirection::LT),
        /*compare_type=*/nativeVar_16
      );
    }
    ::mlir::stablehlo::MulOp tblgen_MulOp_18;
    {
      ::mlir::Value tblgen_value_0 = (*xp1.getODSResults(0).begin());
      ::mlir::Value tblgen_value_1 = (*xp1.getODSResults(0).begin());
      tblgen_MulOp_18 = rewriter.create<::mlir::stablehlo::MulOp>(odsLoc,
        /*lhs=*/tblgen_value_0,
        /*rhs=*/tblgen_value_1
      );
    }
    ::mlir::stablehlo::MulOp square_dekker_high;
    {
      ::mlir::Value tblgen_value_0 = (*y.getODSResults(0).begin());
      ::mlir::Value tblgen_value_1 = (*y.getODSResults(0).begin());
      square_dekker_high = rewriter.create<::mlir::stablehlo::MulOp>(odsLoc,
        /*lhs=*/tblgen_value_0,
        /*rhs=*/tblgen_value_1
      );
    }
    ::mlir::stablehlo::AddOp tblgen_AddOp_19;
    {
      ::mlir::Value tblgen_value_0 = (*tblgen_MulOp_18.getODSResults(0).begin());
      ::mlir::Value tblgen_value_1 = (*square_dekker_high.getODSResults(0).begin());
      tblgen_AddOp_19 = rewriter.create<::mlir::stablehlo::AddOp>(odsLoc,
        /*lhs=*/tblgen_value_0,
        /*rhs=*/tblgen_value_1
      );
    }
    ::mlir::stablehlo::LogOp tblgen_LogOp_20;
    {
      ::mlir::Value tblgen_value_0 = (*tblgen_AddOp_19.getODSResults(0).begin());
      tblgen_LogOp_20 = rewriter.create<::mlir::stablehlo::LogOp>(odsLoc,
        /*operand=*/tblgen_value_0
      );
    }
    ::mlir::stablehlo::MulOp tblgen_MulOp_21;
    {
      ::mlir::Value tblgen_value_0 = half;
      ::mlir::Value tblgen_value_1 = (*tblgen_LogOp_20.getODSResults(0).begin());
      tblgen_MulOp_21 = rewriter.create<::mlir::stablehlo::MulOp>(odsLoc,
        /*lhs=*/tblgen_value_0,
        /*rhs=*/tblgen_value_1
      );
    }
    ::mlir::stablehlo::AddOp x2h;
    {
      ::mlir::Value tblgen_value_0 = (*x.getODSResults(0).begin());
      ::mlir::Value tblgen_value_1 = (*x.getODSResults(0).begin());
      x2h = rewriter.create<::mlir::stablehlo::AddOp>(odsLoc,
        /*lhs=*/tblgen_value_0,
        /*rhs=*/tblgen_value_1
      );
    }
    ::mlir::stablehlo::AddOp _add_2sum_high_2_;
    {
      ::mlir::Value tblgen_value_0 = (*x2h.getODSResults(0).begin());
      ::mlir::Value tblgen_value_1 = (*square_dekker_high.getODSResults(0).begin());
      _add_2sum_high_2_ = rewriter.create<::mlir::stablehlo::AddOp>(odsLoc,
        /*lhs=*/tblgen_value_0,
        /*rhs=*/tblgen_value_1
      );
    }
    ::mlir::stablehlo::MulOp _square_dekker_high_0_;
    {
      ::mlir::Value tblgen_value_0 = (*x.getODSResults(0).begin());
      ::mlir::Value tblgen_value_1 = (*x.getODSResults(0).begin());
      _square_dekker_high_0_ = rewriter.create<::mlir::stablehlo::MulOp>(odsLoc,
        /*lhs=*/tblgen_value_0,
        /*rhs=*/tblgen_value_1
      );
    }
    ::mlir::stablehlo::AddOp _add_2sum_high_1_;
    {
      ::mlir::Value tblgen_value_0 = (*_add_2sum_high_2_.getODSResults(0).begin());
      ::mlir::Value tblgen_value_1 = (*_square_dekker_high_0_.getODSResults(0).begin());
      _add_2sum_high_1_ = rewriter.create<::mlir::stablehlo::AddOp>(odsLoc,
        /*lhs=*/tblgen_value_0,
        /*rhs=*/tblgen_value_1
      );
    }
    ::mlir::stablehlo::NegOp tblgen_NegOp_22;
    {
      ::mlir::Value tblgen_value_0 = (*square_dekker_high.getODSResults(0).begin());
      tblgen_NegOp_22 = rewriter.create<::mlir::stablehlo::NegOp>(odsLoc,
        /*operand=*/tblgen_value_0
      );
    }
    auto nativeVar_23 = ::mlir::stablehlo::getConstantLike(rewriter, odsLoc, 1e+308, (*x.getODSResults(0).begin())); (void)nativeVar_23;
    auto nativeVar_24 = ::mlir::stablehlo::ComparisonTypeAttr(); (void)nativeVar_24;
    ::mlir::stablehlo::CompareOp tblgen_CompareOp_25;
    {
      ::mlir::Value tblgen_value_0 = largest;
      ::mlir::Value tblgen_value_1 = nativeVar_23;
      tblgen_CompareOp_25 = rewriter.create<::mlir::stablehlo::CompareOp>(odsLoc,
        /*lhs=*/tblgen_value_0,
        /*rhs=*/tblgen_value_1,
        ::mlir::stablehlo::ComparisonDirectionAttr::get(rewriter.getContext(), ::mlir::stablehlo::ComparisonDirection::GT),
        /*compare_type=*/nativeVar_24
      );
    }
    auto nativeVar_26 = ::mlir::stablehlo::getConstantLike(rewriter, odsLoc, 134217729, (*x.getODSResults(0).begin())); (void)nativeVar_26;
    auto nativeVar_27 = ::mlir::stablehlo::getConstantLike(rewriter, odsLoc, 1e+38, (*x.getODSResults(0).begin())); (void)nativeVar_27;
    auto nativeVar_28 = ::mlir::stablehlo::ComparisonTypeAttr(); (void)nativeVar_28;
    ::mlir::stablehlo::CompareOp tblgen_CompareOp_29;
    {
      ::mlir::Value tblgen_value_0 = largest;
      ::mlir::Value tblgen_value_1 = nativeVar_27;
      tblgen_CompareOp_29 = rewriter.create<::mlir::stablehlo::CompareOp>(odsLoc,
        /*lhs=*/tblgen_value_0,
        /*rhs=*/tblgen_value_1,
        ::mlir::stablehlo::ComparisonDirectionAttr::get(rewriter.getContext(), ::mlir::stablehlo::ComparisonDirection::GT),
        /*compare_type=*/nativeVar_28
      );
    }
    auto nativeVar_30 = ::mlir::stablehlo::getConstantLike(rewriter, odsLoc, 4097, (*x.getODSResults(0).begin())); (void)nativeVar_30;
    auto nativeVar_31 = ::mlir::stablehlo::getConstantLike(rewriter, odsLoc, 65, (*x.getODSResults(0).begin())); (void)nativeVar_31;
    ::mlir::stablehlo::SelectOp tblgen_SelectOp_32;
    {
      ::mlir::Value tblgen_value_0 = (*tblgen_CompareOp_29.getODSResults(0).begin());
      ::mlir::Value tblgen_value_1 = nativeVar_30;
      ::mlir::Value tblgen_value_2 = nativeVar_31;
      tblgen_SelectOp_32 = rewriter.create<::mlir::stablehlo::SelectOp>(odsLoc,
        /*pred=*/tblgen_value_0,
        /*on_true=*/tblgen_value_1,
        /*on_false=*/tblgen_value_2
      );
    }
    ::mlir::stablehlo::SelectOp veltkamp_splitter_constant;
    {
      ::mlir::Value tblgen_value_0 = (*tblgen_CompareOp_25.getODSResults(0).begin());
      ::mlir::Value tblgen_value_1 = nativeVar_26;
      ::mlir::Value tblgen_value_2 = (*tblgen_SelectOp_32.getODSResults(0).begin());
      veltkamp_splitter_constant = rewriter.create<::mlir::stablehlo::SelectOp>(odsLoc,
        /*pred=*/tblgen_value_0,
        /*on_true=*/tblgen_value_1,
        /*on_false=*/tblgen_value_2
      );
    }
    ::mlir::stablehlo::MulOp multiply_veltkamp_splitter_constant_y;
    {
      ::mlir::Value tblgen_value_0 = (*veltkamp_splitter_constant.getODSResults(0).begin());
      ::mlir::Value tblgen_value_1 = (*y.getODSResults(0).begin());
      multiply_veltkamp_splitter_constant_y = rewriter.create<::mlir::stablehlo::MulOp>(odsLoc,
        /*lhs=*/tblgen_value_0,
        /*rhs=*/tblgen_value_1
      );
    }
    ::mlir::stablehlo::SubtractOp tblgen_SubtractOp_33;
    {
      ::mlir::Value tblgen_value_0 = (*y.getODSResults(0).begin());
      ::mlir::Value tblgen_value_1 = (*multiply_veltkamp_splitter_constant_y.getODSResults(0).begin());
      tblgen_SubtractOp_33 = rewriter.create<::mlir::stablehlo::SubtractOp>(odsLoc,
        /*lhs=*/tblgen_value_0,
        /*rhs=*/tblgen_value_1
      );
    }
    ::mlir::stablehlo::AddOp yh;
    {
      ::mlir::Value tblgen_value_0 = (*multiply_veltkamp_splitter_constant_y.getODSResults(0).begin());
      ::mlir::Value tblgen_value_1 = (*tblgen_SubtractOp_33.getODSResults(0).begin());
      yh = rewriter.create<::mlir::stablehlo::AddOp>(odsLoc,
        /*lhs=*/tblgen_value_0,
        /*rhs=*/tblgen_value_1
      );
    }
    ::mlir::stablehlo::MulOp tblgen_MulOp_34;
    {
      ::mlir::Value tblgen_value_0 = (*yh.getODSResults(0).begin());
      ::mlir::Value tblgen_value_1 = (*yh.getODSResults(0).begin());
      tblgen_MulOp_34 = rewriter.create<::mlir::stablehlo::MulOp>(odsLoc,
        /*lhs=*/tblgen_value_0,
        /*rhs=*/tblgen_value_1
      );
    }
    ::mlir::stablehlo::AddOp tblgen_AddOp_35;
    {
      ::mlir::Value tblgen_value_0 = (*tblgen_NegOp_22.getODSResults(0).begin());
      ::mlir::Value tblgen_value_1 = (*tblgen_MulOp_34.getODSResults(0).begin());
      tblgen_AddOp_35 = rewriter.create<::mlir::stablehlo::AddOp>(odsLoc,
        /*lhs=*/tblgen_value_0,
        /*rhs=*/tblgen_value_1
      );
    }
    ::mlir::stablehlo::SubtractOp yl;
    {
      ::mlir::Value tblgen_value_0 = (*y.getODSResults(0).begin());
      ::mlir::Value tblgen_value_1 = (*yh.getODSResults(0).begin());
      yl = rewriter.create<::mlir::stablehlo::SubtractOp>(odsLoc,
        /*lhs=*/tblgen_value_0,
        /*rhs=*/tblgen_value_1
      );
    }
    ::mlir::stablehlo::MulOp multiply_yh_yl;
    {
      ::mlir::Value tblgen_value_0 = (*yh.getODSResults(0).begin());
      ::mlir::Value tblgen_value_1 = (*yl.getODSResults(0).begin());
      multiply_yh_yl = rewriter.create<::mlir::stablehlo::MulOp>(odsLoc,
        /*lhs=*/tblgen_value_0,
        /*rhs=*/tblgen_value_1
      );
    }
    ::mlir::stablehlo::AddOp tblgen_AddOp_36;
    {
      ::mlir::Value tblgen_value_0 = (*tblgen_AddOp_35.getODSResults(0).begin());
      ::mlir::Value tblgen_value_1 = (*multiply_yh_yl.getODSResults(0).begin());
      tblgen_AddOp_36 = rewriter.create<::mlir::stablehlo::AddOp>(odsLoc,
        /*lhs=*/tblgen_value_0,
        /*rhs=*/tblgen_value_1
      );
    }
    ::mlir::stablehlo::AddOp tblgen_AddOp_37;
    {
      ::mlir::Value tblgen_value_0 = (*tblgen_AddOp_36.getODSResults(0).begin());
      ::mlir::Value tblgen_value_1 = (*multiply_yh_yl.getODSResults(0).begin());
      tblgen_AddOp_37 = rewriter.create<::mlir::stablehlo::AddOp>(odsLoc,
        /*lhs=*/tblgen_value_0,
        /*rhs=*/tblgen_value_1
      );
    }
    ::mlir::stablehlo::MulOp tblgen_MulOp_38;
    {
      ::mlir::Value tblgen_value_0 = (*yl.getODSResults(0).begin());
      ::mlir::Value tblgen_value_1 = (*yl.getODSResults(0).begin());
      tblgen_MulOp_38 = rewriter.create<::mlir::stablehlo::MulOp>(odsLoc,
        /*lhs=*/tblgen_value_0,
        /*rhs=*/tblgen_value_1
      );
    }
    ::mlir::stablehlo::AddOp square_dekker_low;
    {
      ::mlir::Value tblgen_value_0 = (*tblgen_AddOp_37.getODSResults(0).begin());
      ::mlir::Value tblgen_value_1 = (*tblgen_MulOp_38.getODSResults(0).begin());
      square_dekker_low = rewriter.create<::mlir::stablehlo::AddOp>(odsLoc,
        /*lhs=*/tblgen_value_0,
        /*rhs=*/tblgen_value_1
      );
    }
    ::mlir::stablehlo::AddOp _add_2sum_high_0_;
    {
      ::mlir::Value tblgen_value_0 = (*_add_2sum_high_1_.getODSResults(0).begin());
      ::mlir::Value tblgen_value_1 = (*square_dekker_low.getODSResults(0).begin());
      _add_2sum_high_0_ = rewriter.create<::mlir::stablehlo::AddOp>(odsLoc,
        /*lhs=*/tblgen_value_0,
        /*rhs=*/tblgen_value_1
      );
    }
    ::mlir::stablehlo::NegOp tblgen_NegOp_39;
    {
      ::mlir::Value tblgen_value_0 = (*_square_dekker_high_0_.getODSResults(0).begin());
      tblgen_NegOp_39 = rewriter.create<::mlir::stablehlo::NegOp>(odsLoc,
        /*operand=*/tblgen_value_0
      );
    }
    ::mlir::stablehlo::MulOp multiply_veltkamp_splitter_constant_x;
    {
      ::mlir::Value tblgen_value_0 = (*veltkamp_splitter_constant.getODSResults(0).begin());
      ::mlir::Value tblgen_value_1 = (*x.getODSResults(0).begin());
      multiply_veltkamp_splitter_constant_x = rewriter.create<::mlir::stablehlo::MulOp>(odsLoc,
        /*lhs=*/tblgen_value_0,
        /*rhs=*/tblgen_value_1
      );
    }
    ::mlir::stablehlo::SubtractOp tblgen_SubtractOp_40;
    {
      ::mlir::Value tblgen_value_0 = (*x.getODSResults(0).begin());
      ::mlir::Value tblgen_value_1 = (*multiply_veltkamp_splitter_constant_x.getODSResults(0).begin());
      tblgen_SubtractOp_40 = rewriter.create<::mlir::stablehlo::SubtractOp>(odsLoc,
        /*lhs=*/tblgen_value_0,
        /*rhs=*/tblgen_value_1
      );
    }
    ::mlir::stablehlo::AddOp xh;
    {
      ::mlir::Value tblgen_value_0 = (*multiply_veltkamp_splitter_constant_x.getODSResults(0).begin());
      ::mlir::Value tblgen_value_1 = (*tblgen_SubtractOp_40.getODSResults(0).begin());
      xh = rewriter.create<::mlir::stablehlo::AddOp>(odsLoc,
        /*lhs=*/tblgen_value_0,
        /*rhs=*/tblgen_value_1
      );
    }
    ::mlir::stablehlo::MulOp tblgen_MulOp_41;
    {
      ::mlir::Value tblgen_value_0 = (*xh.getODSResults(0).begin());
      ::mlir::Value tblgen_value_1 = (*xh.getODSResults(0).begin());
      tblgen_MulOp_41 = rewriter.create<::mlir::stablehlo::MulOp>(odsLoc,
        /*lhs=*/tblgen_value_0,
        /*rhs=*/tblgen_value_1
      );
    }
    ::mlir::stablehlo::AddOp tblgen_AddOp_42;
    {
      ::mlir::Value tblgen_value_0 = (*tblgen_NegOp_39.getODSResults(0).begin());
      ::mlir::Value tblgen_value_1 = (*tblgen_MulOp_41.getODSResults(0).begin());
      tblgen_AddOp_42 = rewriter.create<::mlir::stablehlo::AddOp>(odsLoc,
        /*lhs=*/tblgen_value_0,
        /*rhs=*/tblgen_value_1
      );
    }
    ::mlir::stablehlo::SubtractOp xl;
    {
      ::mlir::Value tblgen_value_0 = (*x.getODSResults(0).begin());
      ::mlir::Value tblgen_value_1 = (*xh.getODSResults(0).begin());
      xl = rewriter.create<::mlir::stablehlo::SubtractOp>(odsLoc,
        /*lhs=*/tblgen_value_0,
        /*rhs=*/tblgen_value_1
      );
    }
    ::mlir::stablehlo::MulOp multiply_xh_xl;
    {
      ::mlir::Value tblgen_value_0 = (*xh.getODSResults(0).begin());
      ::mlir::Value tblgen_value_1 = (*xl.getODSResults(0).begin());
      multiply_xh_xl = rewriter.create<::mlir::stablehlo::MulOp>(odsLoc,
        /*lhs=*/tblgen_value_0,
        /*rhs=*/tblgen_value_1
      );
    }
    ::mlir::stablehlo::AddOp tblgen_AddOp_43;
    {
      ::mlir::Value tblgen_value_0 = (*tblgen_AddOp_42.getODSResults(0).begin());
      ::mlir::Value tblgen_value_1 = (*multiply_xh_xl.getODSResults(0).begin());
      tblgen_AddOp_43 = rewriter.create<::mlir::stablehlo::AddOp>(odsLoc,
        /*lhs=*/tblgen_value_0,
        /*rhs=*/tblgen_value_1
      );
    }
    ::mlir::stablehlo::AddOp tblgen_AddOp_44;
    {
      ::mlir::Value tblgen_value_0 = (*tblgen_AddOp_43.getODSResults(0).begin());
      ::mlir::Value tblgen_value_1 = (*multiply_xh_xl.getODSResults(0).begin());
      tblgen_AddOp_44 = rewriter.create<::mlir::stablehlo::AddOp>(odsLoc,
        /*lhs=*/tblgen_value_0,
        /*rhs=*/tblgen_value_1
      );
    }
    ::mlir::stablehlo::MulOp tblgen_MulOp_45;
    {
      ::mlir::Value tblgen_value_0 = (*xl.getODSResults(0).begin());
      ::mlir::Value tblgen_value_1 = (*xl.getODSResults(0).begin());
      tblgen_MulOp_45 = rewriter.create<::mlir::stablehlo::MulOp>(odsLoc,
        /*lhs=*/tblgen_value_0,
        /*rhs=*/tblgen_value_1
      );
    }
    ::mlir::stablehlo::AddOp _square_dekker_low_0_;
    {
      ::mlir::Value tblgen_value_0 = (*tblgen_AddOp_44.getODSResults(0).begin());
      ::mlir::Value tblgen_value_1 = (*tblgen_MulOp_45.getODSResults(0).begin());
      _square_dekker_low_0_ = rewriter.create<::mlir::stablehlo::AddOp>(odsLoc,
        /*lhs=*/tblgen_value_0,
        /*rhs=*/tblgen_value_1
      );
    }
    ::mlir::stablehlo::AddOp add_2sum_high;
    {
      ::mlir::Value tblgen_value_0 = (*_add_2sum_high_0_.getODSResults(0).begin());
      ::mlir::Value tblgen_value_1 = (*_square_dekker_low_0_.getODSResults(0).begin());
      add_2sum_high = rewriter.create<::mlir::stablehlo::AddOp>(odsLoc,
        /*lhs=*/tblgen_value_0,
        /*rhs=*/tblgen_value_1
      );
    }
    ::mlir::stablehlo::SubtractOp subtract__add_2sum_high_2__x2h;
    {
      ::mlir::Value tblgen_value_0 = (*_add_2sum_high_2_.getODSResults(0).begin());
      ::mlir::Value tblgen_value_1 = (*x2h.getODSResults(0).begin());
      subtract__add_2sum_high_2__x2h = rewriter.create<::mlir::stablehlo::SubtractOp>(odsLoc,
        /*lhs=*/tblgen_value_0,
        /*rhs=*/tblgen_value_1
      );
    }
    ::mlir::stablehlo::SubtractOp tblgen_SubtractOp_46;
    {
      ::mlir::Value tblgen_value_0 = (*_add_2sum_high_2_.getODSResults(0).begin());
      ::mlir::Value tblgen_value_1 = (*subtract__add_2sum_high_2__x2h.getODSResults(0).begin());
      tblgen_SubtractOp_46 = rewriter.create<::mlir::stablehlo::SubtractOp>(odsLoc,
        /*lhs=*/tblgen_value_0,
        /*rhs=*/tblgen_value_1
      );
    }
    ::mlir::stablehlo::SubtractOp tblgen_SubtractOp_47;
    {
      ::mlir::Value tblgen_value_0 = (*x2h.getODSResults(0).begin());
      ::mlir::Value tblgen_value_1 = (*tblgen_SubtractOp_46.getODSResults(0).begin());
      tblgen_SubtractOp_47 = rewriter.create<::mlir::stablehlo::SubtractOp>(odsLoc,
        /*lhs=*/tblgen_value_0,
        /*rhs=*/tblgen_value_1
      );
    }
    ::mlir::stablehlo::SubtractOp tblgen_SubtractOp_48;
    {
      ::mlir::Value tblgen_value_0 = (*square_dekker_high.getODSResults(0).begin());
      ::mlir::Value tblgen_value_1 = (*subtract__add_2sum_high_2__x2h.getODSResults(0).begin());
      tblgen_SubtractOp_48 = rewriter.create<::mlir::stablehlo::SubtractOp>(odsLoc,
        /*lhs=*/tblgen_value_0,
        /*rhs=*/tblgen_value_1
      );
    }
    ::mlir::stablehlo::AddOp add_2sum_low;
    {
      ::mlir::Value tblgen_value_0 = (*tblgen_SubtractOp_47.getODSResults(0).begin());
      ::mlir::Value tblgen_value_1 = (*tblgen_SubtractOp_48.getODSResults(0).begin());
      add_2sum_low = rewriter.create<::mlir::stablehlo::AddOp>(odsLoc,
        /*lhs=*/tblgen_value_0,
        /*rhs=*/tblgen_value_1
      );
    }
    ::mlir::stablehlo::SubtractOp subtract__add_2sum_high_1___add_2sum_high_2_;
    {
      ::mlir::Value tblgen_value_0 = (*_add_2sum_high_1_.getODSResults(0).begin());
      ::mlir::Value tblgen_value_1 = (*_add_2sum_high_2_.getODSResults(0).begin());
      subtract__add_2sum_high_1___add_2sum_high_2_ = rewriter.create<::mlir::stablehlo::SubtractOp>(odsLoc,
        /*lhs=*/tblgen_value_0,
        /*rhs=*/tblgen_value_1
      );
    }
    ::mlir::stablehlo::SubtractOp tblgen_SubtractOp_49;
    {
      ::mlir::Value tblgen_value_0 = (*_add_2sum_high_1_.getODSResults(0).begin());
      ::mlir::Value tblgen_value_1 = (*subtract__add_2sum_high_1___add_2sum_high_2_.getODSResults(0).begin());
      tblgen_SubtractOp_49 = rewriter.create<::mlir::stablehlo::SubtractOp>(odsLoc,
        /*lhs=*/tblgen_value_0,
        /*rhs=*/tblgen_value_1
      );
    }
    ::mlir::stablehlo::SubtractOp tblgen_SubtractOp_50;
    {
      ::mlir::Value tblgen_value_0 = (*_add_2sum_high_2_.getODSResults(0).begin());
      ::mlir::Value tblgen_value_1 = (*tblgen_SubtractOp_49.getODSResults(0).begin());
      tblgen_SubtractOp_50 = rewriter.create<::mlir::stablehlo::SubtractOp>(odsLoc,
        /*lhs=*/tblgen_value_0,
        /*rhs=*/tblgen_value_1
      );
    }
    ::mlir::stablehlo::SubtractOp tblgen_SubtractOp_51;
    {
      ::mlir::Value tblgen_value_0 = (*_square_dekker_high_0_.getODSResults(0).begin());
      ::mlir::Value tblgen_value_1 = (*subtract__add_2sum_high_1___add_2sum_high_2_.getODSResults(0).begin());
      tblgen_SubtractOp_51 = rewriter.create<::mlir::stablehlo::SubtractOp>(odsLoc,
        /*lhs=*/tblgen_value_0,
        /*rhs=*/tblgen_value_1
      );
    }
    ::mlir::stablehlo::AddOp _add_2sum_low_0_;
    {
      ::mlir::Value tblgen_value_0 = (*tblgen_SubtractOp_50.getODSResults(0).begin());
      ::mlir::Value tblgen_value_1 = (*tblgen_SubtractOp_51.getODSResults(0).begin());
      _add_2sum_low_0_ = rewriter.create<::mlir::stablehlo::AddOp>(odsLoc,
        /*lhs=*/tblgen_value_0,
        /*rhs=*/tblgen_value_1
      );
    }
    ::mlir::stablehlo::AddOp tblgen_AddOp_52;
    {
      ::mlir::Value tblgen_value_0 = (*add_2sum_low.getODSResults(0).begin());
      ::mlir::Value tblgen_value_1 = (*_add_2sum_low_0_.getODSResults(0).begin());
      tblgen_AddOp_52 = rewriter.create<::mlir::stablehlo::AddOp>(odsLoc,
        /*lhs=*/tblgen_value_0,
        /*rhs=*/tblgen_value_1
      );
    }
    ::mlir::stablehlo::SubtractOp subtract__add_2sum_high_0___add_2sum_high_1_;
    {
      ::mlir::Value tblgen_value_0 = (*_add_2sum_high_0_.getODSResults(0).begin());
      ::mlir::Value tblgen_value_1 = (*_add_2sum_high_1_.getODSResults(0).begin());
      subtract__add_2sum_high_0___add_2sum_high_1_ = rewriter.create<::mlir::stablehlo::SubtractOp>(odsLoc,
        /*lhs=*/tblgen_value_0,
        /*rhs=*/tblgen_value_1
      );
    }
    ::mlir::stablehlo::SubtractOp tblgen_SubtractOp_53;
    {
      ::mlir::Value tblgen_value_0 = (*_add_2sum_high_0_.getODSResults(0).begin());
      ::mlir::Value tblgen_value_1 = (*subtract__add_2sum_high_0___add_2sum_high_1_.getODSResults(0).begin());
      tblgen_SubtractOp_53 = rewriter.create<::mlir::stablehlo::SubtractOp>(odsLoc,
        /*lhs=*/tblgen_value_0,
        /*rhs=*/tblgen_value_1
      );
    }
    ::mlir::stablehlo::SubtractOp tblgen_SubtractOp_54;
    {
      ::mlir::Value tblgen_value_0 = (*_add_2sum_high_1_.getODSResults(0).begin());
      ::mlir::Value tblgen_value_1 = (*tblgen_SubtractOp_53.getODSResults(0).begin());
      tblgen_SubtractOp_54 = rewriter.create<::mlir::stablehlo::SubtractOp>(odsLoc,
        /*lhs=*/tblgen_value_0,
        /*rhs=*/tblgen_value_1
      );
    }
    ::mlir::stablehlo::SubtractOp tblgen_SubtractOp_55;
    {
      ::mlir::Value tblgen_value_0 = (*square_dekker_low.getODSResults(0).begin());
      ::mlir::Value tblgen_value_1 = (*subtract__add_2sum_high_0___add_2sum_high_1_.getODSResults(0).begin());
      tblgen_SubtractOp_55 = rewriter.create<::mlir::stablehlo::SubtractOp>(odsLoc,
        /*lhs=*/tblgen_value_0,
        /*rhs=*/tblgen_value_1
      );
    }
    ::mlir::stablehlo::AddOp _add_2sum_low_1_;
    {
      ::mlir::Value tblgen_value_0 = (*tblgen_SubtractOp_54.getODSResults(0).begin());
      ::mlir::Value tblgen_value_1 = (*tblgen_SubtractOp_55.getODSResults(0).begin());
      _add_2sum_low_1_ = rewriter.create<::mlir::stablehlo::AddOp>(odsLoc,
        /*lhs=*/tblgen_value_0,
        /*rhs=*/tblgen_value_1
      );
    }
    ::mlir::stablehlo::AddOp tblgen_AddOp_56;
    {
      ::mlir::Value tblgen_value_0 = (*tblgen_AddOp_52.getODSResults(0).begin());
      ::mlir::Value tblgen_value_1 = (*_add_2sum_low_1_.getODSResults(0).begin());
      tblgen_AddOp_56 = rewriter.create<::mlir::stablehlo::AddOp>(odsLoc,
        /*lhs=*/tblgen_value_0,
        /*rhs=*/tblgen_value_1
      );
    }
    ::mlir::stablehlo::SubtractOp subtract_add_2sum_high__add_2sum_high_0_;
    {
      ::mlir::Value tblgen_value_0 = (*add_2sum_high.getODSResults(0).begin());
      ::mlir::Value tblgen_value_1 = (*_add_2sum_high_0_.getODSResults(0).begin());
      subtract_add_2sum_high__add_2sum_high_0_ = rewriter.create<::mlir::stablehlo::SubtractOp>(odsLoc,
        /*lhs=*/tblgen_value_0,
        /*rhs=*/tblgen_value_1
      );
    }
    ::mlir::stablehlo::SubtractOp tblgen_SubtractOp_57;
    {
      ::mlir::Value tblgen_value_0 = (*add_2sum_high.getODSResults(0).begin());
      ::mlir::Value tblgen_value_1 = (*subtract_add_2sum_high__add_2sum_high_0_.getODSResults(0).begin());
      tblgen_SubtractOp_57 = rewriter.create<::mlir::stablehlo::SubtractOp>(odsLoc,
        /*lhs=*/tblgen_value_0,
        /*rhs=*/tblgen_value_1
      );
    }
    ::mlir::stablehlo::SubtractOp tblgen_SubtractOp_58;
    {
      ::mlir::Value tblgen_value_0 = (*_add_2sum_high_0_.getODSResults(0).begin());
      ::mlir::Value tblgen_value_1 = (*tblgen_SubtractOp_57.getODSResults(0).begin());
      tblgen_SubtractOp_58 = rewriter.create<::mlir::stablehlo::SubtractOp>(odsLoc,
        /*lhs=*/tblgen_value_0,
        /*rhs=*/tblgen_value_1
      );
    }
    ::mlir::stablehlo::SubtractOp tblgen_SubtractOp_59;
    {
      ::mlir::Value tblgen_value_0 = (*_square_dekker_low_0_.getODSResults(0).begin());
      ::mlir::Value tblgen_value_1 = (*subtract_add_2sum_high__add_2sum_high_0_.getODSResults(0).begin());
      tblgen_SubtractOp_59 = rewriter.create<::mlir::stablehlo::SubtractOp>(odsLoc,
        /*lhs=*/tblgen_value_0,
        /*rhs=*/tblgen_value_1
      );
    }
    ::mlir::stablehlo::AddOp _add_2sum_low_2_;
    {
      ::mlir::Value tblgen_value_0 = (*tblgen_SubtractOp_58.getODSResults(0).begin());
      ::mlir::Value tblgen_value_1 = (*tblgen_SubtractOp_59.getODSResults(0).begin());
      _add_2sum_low_2_ = rewriter.create<::mlir::stablehlo::AddOp>(odsLoc,
        /*lhs=*/tblgen_value_0,
        /*rhs=*/tblgen_value_1
      );
    }
    ::mlir::stablehlo::AddOp tblgen_AddOp_60;
    {
      ::mlir::Value tblgen_value_0 = (*tblgen_AddOp_56.getODSResults(0).begin());
      ::mlir::Value tblgen_value_1 = (*_add_2sum_low_2_.getODSResults(0).begin());
      tblgen_AddOp_60 = rewriter.create<::mlir::stablehlo::AddOp>(odsLoc,
        /*lhs=*/tblgen_value_0,
        /*rhs=*/tblgen_value_1
      );
    }
    ::mlir::stablehlo::AddOp sum_2sum_high;
    {
      ::mlir::Value tblgen_value_0 = (*add_2sum_high.getODSResults(0).begin());
      ::mlir::Value tblgen_value_1 = (*tblgen_AddOp_60.getODSResults(0).begin());
      sum_2sum_high = rewriter.create<::mlir::stablehlo::AddOp>(odsLoc,
        /*lhs=*/tblgen_value_0,
        /*rhs=*/tblgen_value_1
      );
    }
    ::mlir::stablehlo::Log1pOp tblgen_Log1pOp_61;
    {
      ::mlir::Value tblgen_value_0 = (*sum_2sum_high.getODSResults(0).begin());
      tblgen_Log1pOp_61 = rewriter.create<::mlir::stablehlo::Log1pOp>(odsLoc,
        /*operand=*/tblgen_value_0
      );
    }
    ::mlir::stablehlo::MulOp tblgen_MulOp_62;
    {
      ::mlir::Value tblgen_value_0 = half;
      ::mlir::Value tblgen_value_1 = (*tblgen_Log1pOp_61.getODSResults(0).begin());
      tblgen_MulOp_62 = rewriter.create<::mlir::stablehlo::MulOp>(odsLoc,
        /*lhs=*/tblgen_value_0,
        /*rhs=*/tblgen_value_1
      );
    }
    ::mlir::stablehlo::SelectOp tblgen_SelectOp_63;
    {
      ::mlir::Value tblgen_value_0 = (*tblgen_CompareOp_17.getODSResults(0).begin());
      ::mlir::Value tblgen_value_1 = (*tblgen_MulOp_21.getODSResults(0).begin());
      ::mlir::Value tblgen_value_2 = (*tblgen_MulOp_62.getODSResults(0).begin());
      tblgen_SelectOp_63 = rewriter.create<::mlir::stablehlo::SelectOp>(odsLoc,
        /*pred=*/tblgen_value_0,
        /*on_true=*/tblgen_value_1,
        /*on_false=*/tblgen_value_2
      );
    }
    ::mlir::stablehlo::SelectOp tblgen_SelectOp_64;
    {
      ::mlir::Value tblgen_value_0 = (*tblgen_CompareOp_4.getODSResults(0).begin());
      ::mlir::Value tblgen_value_1 = (*tblgen_AddOp_12.getODSResults(0).begin());
      ::mlir::Value tblgen_value_2 = (*tblgen_SelectOp_63.getODSResults(0).begin());
      tblgen_SelectOp_64 = rewriter.create<::mlir::stablehlo::SelectOp>(odsLoc,
        /*pred=*/tblgen_value_0,
        /*on_true=*/tblgen_value_1,
        /*on_false=*/tblgen_value_2
      );
    }
    ::mlir::stablehlo::Atan2Op tblgen_Atan2Op_65;
    {
      ::mlir::Value tblgen_value_0 = (*y.getODSResults(0).begin());
      ::mlir::Value tblgen_value_1 = (*xp1.getODSResults(0).begin());
      tblgen_Atan2Op_65 = rewriter.create<::mlir::stablehlo::Atan2Op>(odsLoc,
        /*lhs=*/tblgen_value_0,
        /*rhs=*/tblgen_value_1
      );
    }
    ::mlir::stablehlo::ComplexOp tblgen_ComplexOp_66;
    {
      ::llvm::SmallVector<::mlir::Value, 4> tblgen_values; (void)tblgen_values;
      ::llvm::SmallVector<::mlir::NamedAttribute, 4> tblgen_attrs; (void)tblgen_attrs;
      tblgen_values.push_back((*tblgen_SelectOp_64.getODSResults(0).begin()));
      tblgen_values.push_back((*tblgen_Atan2Op_65.getODSResults(0).begin()));
      ::llvm::SmallVector<::mlir::Type, 4> tblgen_types; (void)tblgen_types;
      for (auto v: castedOp0.getODSResults(0)) {
        tblgen_types.push_back(v.getType());
      }
      tblgen_ComplexOp_66 = rewriter.create<::mlir::stablehlo::ComplexOp>(odsLoc, tblgen_types, tblgen_values, tblgen_attrs);
    }

    for (auto v: ::llvm::SmallVector<::mlir::Value, 4>{ tblgen_ComplexOp_66.getODSResults(0) }) {
      tblgen_repl_values.push_back(v);
    }

    rewriter.replaceOp(op0, tblgen_repl_values);
    return ::mlir::success();
  }
};

void LLVM_ATTRIBUTE_UNUSED populateWithGenerated(::mlir::RewritePatternSet &patterns) {
  patterns.add<Log1pOp_ComplexElementType_ComplexMathExpander>(patterns.getContext());
}
