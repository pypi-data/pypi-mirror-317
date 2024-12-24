// Copyright 2024 MaidSafe.net limited.
//
// This SAFE Network Software is licensed to you under The General Public License (GPL), version 3.
// Unless required by applicable law or agreed to in writing, the SAFE Network Software distributed
// under the GPL Licence is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
// KIND, either express or implied. Please review the Licences for the specific language governing
// permissions and limitations relating to use of the SAFE Network Software.

use crate::common::U256;
use serde::{Deserialize, Serialize};
use std::fmt::{Debug, Formatter, Result as FmtResult};

/// Quoting metrics used to generate a quote, or to track peer's status.
#[derive(Clone, Eq, PartialEq, PartialOrd, Ord, Hash, Serialize, Deserialize)]
pub struct QuotingMetrics {
    /// the records stored
    pub close_records_stored: usize,
    /// the max_records configured
    pub max_records: usize,
    /// number of times that got paid
    pub received_payment_count: usize,
    /// the duration that node keeps connected to the network, measured in hours
    pub live_time: u64,
    /// network density from this node's perspective, which is the responsible_range as well
    /// This could be calculated via sampling, or equation calculation.
    pub network_density: Option<[u8; 32]>,
    /// estimated network size
    pub network_size: Option<u64>,
}

impl QuotingMetrics {
    /// construct an empty QuotingMetrics
    pub fn new() -> Self {
        Self {
            close_records_stored: 0,
            max_records: 0,
            received_payment_count: 0,
            live_time: 0,
            network_density: None,
            network_size: None,
        }
    }
}

impl Default for QuotingMetrics {
    fn default() -> Self {
        Self::new()
    }
}

impl Debug for QuotingMetrics {
    fn fmt(&self, formatter: &mut Formatter) -> FmtResult {
        let density_u256 = self.network_density.map(U256::from_be_bytes);

        write!(formatter, "QuotingMetrics {{ close_records_stored: {}, max_records: {}, received_payment_count: {}, live_time: {}, network_density: {density_u256:?}, network_size: {:?} }}",
               self.close_records_stored, self.max_records, self.received_payment_count, self.live_time, self.network_size)
    }
}
