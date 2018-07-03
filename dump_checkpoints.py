# Copyright 2017 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""A script to dump tensorflow checkpoint variables to deeplearnjs.
This script takes a checkpoint file and writes all of the variables in the
checkpoint to a directory.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import json
import os
import re
import string
import tensorflow as tf

FILENAME_CHARS = string.ascii_letters + string.digits + '_'

def _var_name_to_filename(var_name):
  chars = []
  for c in var_name:
    if c in FILENAME_CHARS:
      chars.append(c)
    elif c == '/':
      chars.append('_')
  return ''.join(chars)

def remove_optimizer_variables(output):
  vars_dir = os.path.expanduser(output)
  manifest_file = os.path.join(output, 'manifest.json')
  with open(manifest_file) as f:
    manifest = json.load(f)
  new_manifest = {key: manifest[key] for key in manifest 
  if 'Adam' not in key and 'beta' not in key}
  with open(manifest_file, 'w') as f:
    json.dump(new_manifest, f, indent=2, sort_keys=True)

  for name in os.listdir(output):
    if 'Adam' in name or 'beta' in name:
      os.remove(os.path.join(output, name))

def dump_checkpoints(checkpoint_dir, output):
  chk_fpath = os.path.expanduser(checkpoint_dir)
  reader = tf.train.NewCheckpointReader(chk_fpath)
  var_to_shape_map = reader.get_variable_to_shape_map()
  output_dir = os.path.expanduser(output)
  tf.gfile.MakeDirs(output_dir)
  manifest = {}
  remove_vars_compiled_re = re.compile('')

  var_filenames_strs = []
  for name in var_to_shape_map:
    if ('' and
        re.match(remove_vars_compiled_re, name)) or name == 'global_step':
      continue
    var_filename = _var_name_to_filename(name)
    manifest[name] = {'filename': var_filename, 'shape': var_to_shape_map[name]}

    tensor = reader.get_tensor(name)
    with open(os.path.join(output_dir, var_filename), 'wb') as f:
      f.write(tensor.tobytes())

    var_filenames_strs.append("\"" + var_filename + "\"")

  manifest_fpath = os.path.join(output_dir, 'manifest.json')
  print('Writing manifest to ' + manifest_fpath)
  with open(manifest_fpath, 'w') as f:
    f.write(json.dumps(manifest, indent=2, sort_keys=True))

  remove_optimizer_variables(output_dir)
  