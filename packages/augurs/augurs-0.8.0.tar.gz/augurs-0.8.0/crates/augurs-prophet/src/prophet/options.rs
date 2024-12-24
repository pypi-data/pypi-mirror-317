//! Options to configure a Prophet model.
//!
//! These correspond very closely to the options in the Python
//! implementation, but are not identical; some have been updated
//! to be more idiomatic Rust.

use std::{collections::HashMap, num::NonZeroU32};

use crate::{Error, FeatureMode, Holiday, PositiveFloat, TimestampSeconds, TrendIndicator};

/// The type of growth to use.
#[derive(Clone, Copy, Debug, Eq, PartialEq, Default)]
pub enum GrowthType {
    /// Linear growth (default).
    #[default]
    Linear,
    /// Logistic growth.
    Logistic,
    /// Flat growth.
    Flat,
}

impl From<GrowthType> for TrendIndicator {
    fn from(value: GrowthType) -> Self {
        match value {
            GrowthType::Linear => TrendIndicator::Linear,
            GrowthType::Logistic => TrendIndicator::Logistic,
            GrowthType::Flat => TrendIndicator::Flat,
        }
    }
}

/// Define whether to include a specific seasonality, and how it should be specified.
#[derive(Clone, Copy, Debug, Default)]
pub enum SeasonalityOption {
    /// Automatically determine whether to include this seasonality.
    ///
    /// Yearly seasonality is automatically included if there is >=2
    /// years of history.
    ///
    /// Weekly seasonality is automatically included if there is >=2
    /// weeks of history, and the spacing between the dates in the
    /// data is <7 days.
    ///
    /// Daily seasonality is automatically included if there is >=2
    /// days of history, and the spacing between the dates in the
    /// data is <1 day.
    #[default]
    Auto,
    /// Manually specify whether to include this seasonality.
    Manual(bool),
    /// Enable this seasonality and use the provided number of Fourier terms.
    Fourier(NonZeroU32),
}

/// How to scale the data prior to fitting the model.
#[derive(Clone, Copy, Debug, Eq, PartialEq, Default)]
pub enum Scaling {
    /// Use abs-max scaling (the default).
    #[default]
    AbsMax,
    /// Use min-max scaling.
    MinMax,
}

/// How to do parameter estimation.
///
/// Note: for now, only MLE/MAP estimation is supported, i.e. there
/// is no support for MCMC sampling. This will be added in the future!
/// The enum will be marked as `non_exhaustive` until that point.
#[derive(Clone, Debug, Copy, PartialEq, Eq, Default)]
#[non_exhaustive]
pub enum EstimationMode {
    /// Use MLE estimation.
    #[default]
    Mle,
    /// Use MAP estimation.
    Map,
    // This is not yet implemented. We need to add a new `Sampler` trait and
    // implement it, then handle the different number outputs when predicting,
    // before this can be enabled.
    // /// Do full Bayesian inference with the specified number of MCMC samples.
    //
    // Mcmc(u32),
}

/// The width of the uncertainty intervals.
///
/// Must be between `0.0` and `1.0`. Common values are
/// `0.8` (80%), `0.9` (90%) and `0.95` (95%).
///
/// Defaults to `0.8` for 80% intervals.
#[derive(Debug, Clone, Copy, PartialEq, PartialOrd)]
pub struct IntervalWidth(f64);

impl Default for IntervalWidth {
    fn default() -> Self {
        Self(0.8)
    }
}

impl IntervalWidth {
    /// Attempt to create a new `IntervalWidth `.
    ///
    /// # Errors
    ///
    /// Returns an error if the provided float is less than 0.0.
    pub fn try_new(f: f64) -> Result<Self, Error> {
        if !f.is_finite() || f <= 0.0 {
            return Err(Error::InvalidIntervalWidth(f));
        }
        Ok(Self(f))
    }
}

impl TryFrom<f64> for IntervalWidth {
    type Error = Error;
    fn try_from(value: f64) -> Result<Self, Self::Error> {
        Self::try_new(value)
    }
}

impl std::ops::Deref for IntervalWidth {
    type Target = f64;
    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

impl From<IntervalWidth> for f64 {
    fn from(value: IntervalWidth) -> Self {
        value.0
    }
}

// TODO: consider getting rid of this? It's a bit weird, but it might
// make it easier for users of the crate...
/// Optional version of Prophet's options, before applying any defaults.
#[derive(Default, Debug, Clone)]
pub struct OptProphetOptions {
    /// The type of growth (trend) to use.
    pub growth: Option<GrowthType>,

    /// An optional list of changepoints.
    ///
    /// If not provided, changepoints will be automatically selected.
    pub changepoints: Option<Vec<TimestampSeconds>>,

    /// The number of potential changepoints to include.
    ///
    /// Not used if `changepoints` is provided.
    ///
    /// If provided and `changepoints` is not provided, then
    /// `n_changepoints` potential changepoints will be selected
    /// uniformly from the first `changepoint_range` proportion of
    /// the history.
    pub n_changepoints: Option<u32>,

    /// The proportion of the history to consider for potential changepoints.
    ///
    /// Not used if `changepoints` is provided.
    pub changepoint_range: Option<PositiveFloat>,

    /// How to fit yearly seasonality.
    pub yearly_seasonality: Option<SeasonalityOption>,
    /// How to fit weekly seasonality.
    pub weekly_seasonality: Option<SeasonalityOption>,
    /// How to fit daily seasonality.
    pub daily_seasonality: Option<SeasonalityOption>,

    /// How to model seasonality.
    pub seasonality_mode: Option<FeatureMode>,

    /// The prior scale for seasonality.
    ///
    /// This modulates the strength of seasonality,
    /// with larger values allowing the model to fit
    /// larger seasonal fluctuations and smaller values
    /// dampening the seasonality.
    ///
    /// Can be specified for individual seasonalities
    /// using [`Prophet::add_seasonality`](crate::Prophet::add_seasonality).
    pub seasonality_prior_scale: Option<PositiveFloat>,

    /// The prior scale for changepoints.
    ///
    /// This modulates the flexibility of the automatic
    /// changepoint selection. Large values will allow many
    /// changepoints, while small values will allow few
    /// changepoints.
    pub changepoint_prior_scale: Option<PositiveFloat>,

    /// How to perform parameter estimation.
    ///
    /// When [`EstimationMode::Mle`] or [`EstimationMode::Map`]
    /// are used then no MCMC samples are taken.
    pub estimation: Option<EstimationMode>,

    /// The width of the uncertainty intervals.
    ///
    /// Must be between `0.0` and `1.0`. Common values are
    /// `0.8` (80%), `0.9` (90%) and `0.95` (95%).
    pub interval_width: Option<IntervalWidth>,

    /// The number of simulated draws used to estimate uncertainty intervals.
    ///
    /// Setting this value to `0` will disable uncertainty
    /// estimation and speed up the calculation.
    pub uncertainty_samples: Option<u32>,

    /// How to scale the data prior to fitting the model.
    pub scaling: Option<Scaling>,

    /// Holidays to include in the model.
    pub holidays: Option<HashMap<String, Holiday>>,
    /// Prior scale for holidays.
    ///
    /// This parameter modulates the strength of the holiday
    /// components model, unless overridden in each individual
    /// holiday's input.
    pub holidays_prior_scale: Option<PositiveFloat>,

    /// How to model holidays.
    pub holidays_mode: Option<FeatureMode>,
}

impl From<OptProphetOptions> for ProphetOptions {
    fn from(value: OptProphetOptions) -> Self {
        let defaults = ProphetOptions::default();
        ProphetOptions {
            growth: value.growth.unwrap_or(defaults.growth),
            changepoints: value.changepoints,
            n_changepoints: value.n_changepoints.unwrap_or(defaults.n_changepoints),
            changepoint_range: value
                .changepoint_range
                .unwrap_or(defaults.changepoint_range),
            yearly_seasonality: value
                .yearly_seasonality
                .unwrap_or(defaults.yearly_seasonality),
            weekly_seasonality: value
                .weekly_seasonality
                .unwrap_or(defaults.weekly_seasonality),
            daily_seasonality: value
                .daily_seasonality
                .unwrap_or(defaults.daily_seasonality),
            seasonality_mode: value.seasonality_mode.unwrap_or(defaults.seasonality_mode),
            seasonality_prior_scale: value
                .seasonality_prior_scale
                .unwrap_or(defaults.seasonality_prior_scale),
            changepoint_prior_scale: value
                .changepoint_prior_scale
                .unwrap_or(defaults.changepoint_prior_scale),
            estimation: value.estimation.unwrap_or(defaults.estimation),
            interval_width: value.interval_width.unwrap_or(defaults.interval_width),
            uncertainty_samples: value
                .uncertainty_samples
                .unwrap_or(defaults.uncertainty_samples),
            scaling: value.scaling.unwrap_or(defaults.scaling),
            holidays: value.holidays.unwrap_or(defaults.holidays),
            holidays_prior_scale: value
                .holidays_prior_scale
                .unwrap_or(defaults.holidays_prior_scale),
            holidays_mode: value.holidays_mode,
        }
    }
}

/// Options for Prophet, after applying defaults.
#[derive(Debug, Clone)]
pub struct ProphetOptions {
    /// The type of growth (trend) to use.
    ///
    /// Defaults to [`GrowthType::Linear`].
    pub growth: GrowthType,

    /// An optional list of changepoints.
    ///
    /// If not provided, changepoints will be automatically selected.
    pub changepoints: Option<Vec<TimestampSeconds>>,

    /// The number of potential changepoints to include.
    ///
    /// Not used if `changepoints` is provided.
    ///
    /// If provided and `changepoints` is not provided, then
    /// `n_changepoints` potential changepoints will be selected
    /// uniformly from the first `changepoint_range` proportion of
    /// the history.
    ///
    /// Defaults to 25.
    pub n_changepoints: u32,

    /// The proportion of the history to consider for potential changepoints.
    ///
    /// Not used if `changepoints` is provided.
    ///
    /// Defaults to `0.8` for the first 80% of the data.
    pub changepoint_range: PositiveFloat,

    /// How to fit yearly seasonality.
    ///
    /// Defaults to [`SeasonalityOption::Auto`].
    pub yearly_seasonality: SeasonalityOption,
    /// How to fit weekly seasonality.
    ///
    /// Defaults to [`SeasonalityOption::Auto`].
    pub weekly_seasonality: SeasonalityOption,
    /// How to fit daily seasonality.
    ///
    /// Defaults to [`SeasonalityOption::Auto`].
    pub daily_seasonality: SeasonalityOption,

    /// How to model seasonality.
    ///
    /// Defaults to [`FeatureMode::Additive`].
    pub seasonality_mode: FeatureMode,

    /// The prior scale for seasonality.
    ///
    /// This modulates the strength of seasonality,
    /// with larger values allowing the model to fit
    /// larger seasonal fluctuations and smaller values
    /// dampening the seasonality.
    ///
    /// Can be specified for individual seasonalities
    /// using [`Prophet::add_seasonality`](crate::Prophet::add_seasonality).
    ///
    /// Defaults to `10.0`.
    pub seasonality_prior_scale: PositiveFloat,

    /// The prior scale for changepoints.
    ///
    /// This modulates the flexibility of the automatic
    /// changepoint selection. Large values will allow many
    /// changepoints, while small values will allow few
    /// changepoints.
    ///
    /// Defaults to `0.05`.
    pub changepoint_prior_scale: PositiveFloat,

    /// How to perform parameter estimation.
    ///
    /// When [`EstimationMode::Mle`] or [`EstimationMode::Map`]
    /// are used then no MCMC samples are taken.
    ///
    /// Defaults to [`EstimationMode::Mle`].
    pub estimation: EstimationMode,

    /// The width of the uncertainty intervals.
    ///
    /// Must be between `0.0` and `1.0`. Common values are
    /// `0.8` (80%), `0.9` (90%) and `0.95` (95%).
    ///
    /// Defaults to `0.8` for 80% intervals.
    pub interval_width: IntervalWidth,

    /// The number of simulated draws used to estimate uncertainty intervals.
    ///
    /// Setting this value to `0` will disable uncertainty
    /// estimation and speed up the calculation.
    ///
    /// Defaults to `1000`.
    pub uncertainty_samples: u32,

    /// How to scale the data prior to fitting the model.
    ///
    /// Defaults to [`Scaling::AbsMax`].
    pub scaling: Scaling,

    /// Holidays to include in the model.
    pub holidays: HashMap<String, Holiday>,
    /// Prior scale for holidays.
    ///
    /// This parameter modulates the strength of the holiday
    /// components model, unless overridden in each individual
    /// holiday's input.
    ///
    /// Defaults to `100.0`.
    pub holidays_prior_scale: PositiveFloat,

    /// How to model holidays.
    ///
    /// Defaults to the same value as [`ProphetOptions::seasonality_mode`].
    pub holidays_mode: Option<FeatureMode>,
}

impl Default for ProphetOptions {
    fn default() -> Self {
        Self {
            growth: GrowthType::Linear,
            changepoints: None,
            n_changepoints: 25,
            changepoint_range: 0.8.try_into().unwrap(),
            yearly_seasonality: SeasonalityOption::default(),
            weekly_seasonality: SeasonalityOption::default(),
            daily_seasonality: SeasonalityOption::default(),
            seasonality_mode: FeatureMode::Additive,
            seasonality_prior_scale: 10.0.try_into().unwrap(),
            changepoint_prior_scale: 0.05.try_into().unwrap(),
            estimation: EstimationMode::Mle,
            interval_width: IntervalWidth::default(),
            uncertainty_samples: 1000,
            scaling: Scaling::AbsMax,
            holidays: HashMap::new(),
            holidays_prior_scale: 100.0.try_into().unwrap(),
            holidays_mode: None,
        }
    }
}
