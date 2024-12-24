"""
  Copyright (c) 2024 Vipas.AI

  All rights reserved. This program and the accompanying materials
  are made available under the terms of a proprietary license which prohibits
  redistribution and use in any form, without the express prior written consent
  of Vipas.AI.
  
  This code is proprietary to Vipas.AI and is protected by copyright and
  other intellectual property laws. You may not modify, reproduce, perform,
  display, create derivative works from, repurpose, or distribute this code or any portion of it
  without the express prior written permission of Vipas.AI.
  
  For more information, contact Vipas.AI at legal@vipas.ai
""" 
# List of allowed model framework types
ALLOWED_MODEL_FRAMEWORK_TYPES = [
    "onnx",
    "pytorch",
    "tensorflow",
    "sklearn",
    "xgboost",
    'hugging_face_qwen_2.5',
    'hugging_face_llama_3',
    'hugging_face_google_t5',
    'hugging_face_google_mt5',
    'hugging_face_coedit_large',
    'hugging_face_dslim_bert',
    'hugging_face_distilbert',
]